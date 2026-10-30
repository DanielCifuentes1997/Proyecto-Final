import os
import sys
import json
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from preprocesamiento.texto import preprocesar, tokenizar
from similitud.levenshtein import similitud_levenshtein, matriz_levenshtein
from similitud.jaccard import similitud_jaccard, conjunto
from similitud.dice import similitud_dice
from similitud.tfidf_coseno import ModeloTFIDF, frecuencias, coseno, producto_punto, magnitud
from similitud.ia_embeddings import similitud_coseno, distancia_euclidiana
from clustering.jerarquico import clustering_jerarquico, cortar_en_grupos, CRITERIOS
from clustering.metrica import correlacion_cofenetica
from clustering.dendrograma import orden_de_hojas
from busqueda.buscador import ALGORITMOS as ALG_BUSQUEDA, minusculas, preprocesar_patron, buscar_en_texto
from busqueda.kmp import tabla_prefijos, buscar_kmp
from busqueda.boyer_moore import tabla_caracter_malo, buscar_boyer_moore
from busqueda.rabin_karp import preparar_patron, buscar_rabin_karp, BASE, PRIMO

CORPUS = os.path.join(RAIZ, "datos", "corpus.json")
EMBEDDINGS = os.path.join(RAIZ, "datos", "embeddings.json")
GRUPOS_MAPA = 4
LARGO_FRAGMENTO = 14


class Servicio:
    """Carga el corpus una vez y deja calculado todo lo que usa la página."""

    def __init__(self):
        self.cargar()

    def cargar(self):
        with open(CORPUS, encoding="utf-8") as f:
            self.corpus = json.load(f)
        self.embeddings = {"modelos": {}, "minilm": {}, "glove": {}}
        if os.path.exists(EMBEDDINGS):
            with open(EMBEDDINGS, encoding="utf-8") as f:
                self.embeddings = json.load(f)
        self.recalcular()

    def recalcular(self):
        self.por_id = {}
        abstracts = []
        for art in self.corpus:
            self.por_id[art["id"]] = art
            abstracts.append(art["abstract"])
        self.tfidf = ModeloTFIDF(abstracts)
        self.vectores = []
        for texto in abstracts:
            self.vectores.append(self.tfidf.vector(texto))
        n = len(abstracts)
        self.D = []
        for i in range(n):
            fila = []
            for j in range(n):
                fila.append(0.0)
            self.D.append(fila)
        for i in range(n):
            for j in range(i + 1, n):
                d = 1 - coseno(self.vectores[i], self.vectores[j])
                self.D[i][j] = d
                self.D[j][i] = d
        self.clustering = {}
        for criterio in CRITERIOS:
            inicio = time.perf_counter()
            fusiones = clustering_jerarquico(self.D, criterio) if n > 1 else []
            segundos = time.perf_counter() - inicio
            self.clustering[criterio] = {
                "fusiones": fusiones,
                "segundos": segundos,
                "cofenetica": correlacion_cofenetica(self.D, fusiones) if n > 2 else 0.0,
            }

    # ---------- corpus ----------
    def resumen_corpus(self):
        palabras = 0
        vocabulario = {}
        autores = {}
        articulos = []
        for art in self.corpus:
            tokens = tokenizar(art["abstract"])
            palabras = palabras + len(tokens)
            for p in preprocesar(art["abstract"]):
                vocabulario[p] = True
            for a in art["autores"]:
                autores[a] = True
            articulos.append({
                "id": art["id"], "titulo": art["titulo"], "autores": art["autores"],
                "abstract": art["abstract"], "palabras": len(tokens), "caracteres": len(art["abstract"]),
            })
        return {"articulos": articulos, "total_palabras": palabras, "vocabulario": len(vocabulario),
                "autores": len(autores)}

    def mapa(self):
        """Matriz de similitud TF-IDF y grupos (average linkage) para la vista general."""
        n = len(self.corpus)
        ids = []
        for art in self.corpus:
            ids.append(art["id"])
        k = GRUPOS_MAPA if n >= GRUPOS_MAPA else n
        grupos = cortar_en_grupos(self.clustering["average"]["fusiones"], n, k) if n > 1 else [0] * n
        similitud = []
        for i in range(n):
            fila = []
            for j in range(n):
                fila.append(1.0 if i == j else round(1 - self.D[i][j], 4))
            similitud.append(fila)
        return {"ids": ids, "similitud": similitud, "grupos": grupos}

    # ---------- requerimiento 1 ----------
    def comparar(self, ids):
        pares = []
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                pares.append(self.comparar_par(ids[i], ids[j]))
        return {"pares": pares}

    def comparar_par(self, id_a, id_b):
        a = self.por_id[id_a]["abstract"]
        b = self.por_id[id_b]["abstract"]
        resultados = []

        def medir(nombre, tipo, funcion):
            inicio = time.perf_counter()
            valor = funcion()
            resultados.append({"algoritmo": nombre, "tipo": tipo, "valor": valor,
                               "segundos": time.perf_counter() - inicio})

        medir("Levenshtein", "clasico", lambda: similitud_levenshtein(a, b))
        medir("Jaccard", "clasico", lambda: similitud_jaccard(a, b))
        medir("Dice", "clasico", lambda: similitud_dice(a, b))
        medir("TF-IDF + coseno", "clasico", lambda: self.tfidf.similitud(a, b))
        for clave, nombre in [("minilm", "MiniLM"), ("glove", "GloVe")]:
            va = self.embeddings.get(clave, {}).get(str(id_a))
            vb = self.embeddings.get(clave, {}).get(str(id_b))
            if va is not None and vb is not None:
                medir(nombre, "ia", lambda: similitud_coseno(va, vb))
                resultados[-1]["euclidiana"] = distancia_euclidiana(va, vb)
            else:
                resultados.append({"algoritmo": nombre, "tipo": "ia", "valor": None, "segundos": 0})
        return {"a": id_a, "b": id_b, "resultados": resultados, "detalle": self.detalle_par(a, b)}

    def detalle_par(self, a, b):
        """Datos para mostrar el paso a paso: palabras comunes, pesos TF-IDF y matriz de Levenshtein."""
        A = conjunto(preprocesar(a))
        B = conjunto(preprocesar(b))
        comunes = []
        for p in A:
            if p in B:
                comunes.append(p)
        tfa = frecuencias(preprocesar(a))
        tfb = frecuencias(preprocesar(b))
        va = self.tfidf.vector(a)
        vb = self.tfidf.vector(b)
        tabla = []
        for p in comunes:
            tabla.append({"palabra": p, "tf_a": tfa[p], "tf_b": tfb[p], "df": self.tfidf.df.get(p, 0),
                          "idf": self.tfidf.idf.get(p, 0.0), "peso_a": va.get(p, 0.0), "peso_b": vb.get(p, 0.0),
                          "producto": va.get(p, 0.0) * vb.get(p, 0.0)})
        tabla.sort(key=lambda fila: fila["producto"], reverse=True)
        fa = minusculas(a[:LARGO_FRAGMENTO])
        fb = minusculas(b[:LARGO_FRAGMENTO])
        return {
            "tam_a": len(A), "tam_b": len(B), "comunes": comunes, "tfidf": tabla,
            "n_documentos": self.tfidf.N, "producto_punto": producto_punto(va, vb),
            "magnitud_a": magnitud(va), "magnitud_b": magnitud(vb),
            "levenshtein": {"a": fa, "b": fb, "matriz": matriz_levenshtein(fa, fb),
                            "casillas_completas": (len(a) + 1) * (len(b) + 1)},
        }

    # ---------- requerimiento 2 ----------
    def resultado_clustering(self):
        n = len(self.corpus)
        etiquetas = []
        for art in self.corpus:
            etiquetas.append({"id": art["id"], "titulo": art["titulo"]})
        salida = {"etiquetas": etiquetas, "criterios": []}
        for criterio in CRITERIOS:
            datos = self.clustering[criterio]
            fusiones = []
            for a, b, distancia, nuevo in datos["fusiones"]:
                fusiones.append({"a": a, "b": b, "distancia": distancia, "tamano": len(nuevo)})
            salida["criterios"].append({
                "criterio": criterio, "cofenetica": datos["cofenetica"], "segundos": datos["segundos"],
                "fusiones": fusiones, "orden": orden_de_hojas(datos["fusiones"], n) if n > 1 else [0],
            })
        return salida

    # ---------- requerimiento 3 ----------
    def recorrido(self, patron, textos, encontrados):
        """Paso a paso de los 3 algoritmos sobre un fragmento corto alrededor de la primera coincidencia."""
        if len(encontrados) == 0 or len(patron) == 0:
            return None
        id_art = None
        for clave in encontrados:
            id_art = clave
            break
        texto = textos[id_art]
        pos = encontrados[id_art][0]
        inicio = pos - 20
        if inicio < 0:
            inicio = 0
        fin = pos + len(patron) + 20
        if fin > len(texto):
            fin = len(texto)
        fragmento = texto[inicio:fin]
        pasos_kmp = []
        pasos_bm = []
        pasos_rk = []
        buscar_kmp(fragmento, patron, pasos=pasos_kmp)
        buscar_boyer_moore(fragmento, patron, pasos=pasos_bm)
        buscar_rabin_karp(fragmento, patron, pasos=pasos_rk)
        return {
            "id": id_art, "inicio": inicio, "fragmento": fragmento,
            "kmp": [{"i": i, "j": j, "igual": igual} for i, j, ct, cp, igual in pasos_kmp],
            "boyer_moore": [{"s": s, "j": j, "malo": malo, "salto": salto} for s, j, malo, salto in pasos_bm],
            "rabin_karp": [{"s": s, "hash": h, "coincide_hash": eq, "iguales": ig} for s, h, eq, ig in pasos_rk],
        }

    def buscar(self, patron, repeticiones=10):
        patron = minusculas(patron)
        textos = {}
        for art in self.corpus:
            textos[art["id"]] = minusculas(art["abstract"])
        algoritmos = []
        encontrados_kmp = {}
        for alg in ALG_BUSQUEDA:
            inicio = time.perf_counter()
            for r in range(repeticiones):
                tabla = preprocesar_patron(alg, patron)
            t_pre = (time.perf_counter() - inicio) / repeticiones
            inicio = time.perf_counter()
            for r in range(repeticiones):
                encontrados = {}
                colisiones = 0
                for id_art in textos:
                    posiciones, col = buscar_en_texto(alg, textos[id_art], patron, tabla)
                    colisiones = colisiones + col
                    if len(posiciones) > 0:
                        encontrados[id_art] = posiciones
            t_busq = (time.perf_counter() - inicio) / repeticiones
            total = 0
            for id_art in encontrados:
                total = total + len(encontrados[id_art])
            algoritmos.append({"algoritmo": alg, "ocurrencias": total, "articulos": len(encontrados),
                               "colisiones": colisiones, "t_preprocesamiento": t_pre, "t_busqueda": t_busq})
            if alg == "KMP":
                encontrados_kmp = encontrados
        coincidencias = []
        for id_art in encontrados_kmp:
            coincidencias.append({"id": id_art, "titulo": self.por_id[id_art]["titulo"],
                                  "texto": self.por_id[id_art]["abstract"], "posiciones": encontrados_kmp[id_art]})
        hash_patron, potencia = preparar_patron(patron) if len(patron) > 0 else (0, 1)
        return {
            "patron": patron, "m": len(patron), "algoritmos": algoritmos, "coincidencias": coincidencias,
            "recorrido": self.recorrido(patron, textos, encontrados_kmp),
            "tablas": {"lps": tabla_prefijos(patron) if len(patron) > 0 else [],
                       "caracter_malo": tabla_caracter_malo(patron),
                       "hash": hash_patron, "potencia": potencia, "base": BASE, "primo": PRIMO},
        }
