import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocesamiento.texto import preprocesar
from similitud.levenshtein import matriz_levenshtein
from similitud.jaccard import conjunto
from similitud.tfidf_coseno import frecuencias, producto_punto, magnitud
from similitud.comparar import Comparador, ALGORITMOS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(RAIZ, "salidas", "req1")

ID_A = 11
ID_B = 16
LARGO_FRAGMENTO = 15


def tabla_md(encabezado, filas):
    lineas = ["| " + " | ".join(encabezado) + " |", "|" + "---|" * len(encabezado)]
    for fila in filas:
        lineas.append("| " + " | ".join(str(x) for x in fila) + " |")
    return "\n".join(lineas)


def seccion_levenshtein(a, b):
    fa = a[:LARGO_FRAGMENTO].lower()
    fb = b[:LARGO_FRAGMENTO].lower()
    D = matriz_levenshtein(fa, fb)
    encabezado = ["", "ε"] + [c if c != " " else "␣" for c in fb]
    filas = []
    for i in range(len(fa) + 1):
        letra = "ε" if i == 0 else (fa[i - 1] if fa[i - 1] != " " else "␣")
        filas.append([letra] + D[i])
    texto = ["## 1. Levenshtein", "",
             "Fragmento A (primeros %d caracteres del art. %d): \"%s\"" % (LARGO_FRAGMENTO, ID_A, fa),
             "Fragmento B (primeros %d caracteres del art. %d): \"%s\"" % (LARGO_FRAGMENTO, ID_B, fb), "",
             tabla_md(encabezado, filas), "",
             "Distancia del fragmento = D[%d][%d] = %d" % (len(fa), len(fb), D[len(fa)][len(fb)]),
             "Similitud del fragmento = 1 - %d/%d = %.4f" % (D[len(fa)][len(fb)], max(len(fa), len(fb)),
                                                            1 - D[len(fa)][len(fb)] / max(len(fa), len(fb))),
             "Tamaño de la matriz con los abstracts completos: %d x %d = %d casillas" % (
                 len(a) + 1, len(b) + 1, (len(a) + 1) * (len(b) + 1)), ""]
    return "\n".join(texto)


def seccion_conjuntos(a, b):
    A = conjunto(preprocesar(a))
    B = conjunto(preprocesar(b))
    comunes = []
    for p in A:
        if p in B:
            comunes.append(p)
    union = len(A) + len(B) - len(comunes)
    texto = ["## 2 y 3. Jaccard y Dice", "",
             "|A| (palabras distintas del art. %d) = %d" % (ID_A, len(A)),
             "|B| (palabras distintas del art. %d) = %d" % (ID_B, len(B)),
             "A ∩ B = %d palabras: %s" % (len(comunes), ", ".join(comunes)),
             "|A ∪ B| = %d + %d - %d = %d" % (len(A), len(B), len(comunes), union), "",
             "Jaccard = %d / %d = %.4f" % (len(comunes), union, len(comunes) / union),
             "Dice = 2·%d / (%d + %d) = %d / %d = %.4f" % (len(comunes), len(A), len(B), 2 * len(comunes),
                                                           len(A) + len(B), 2 * len(comunes) / (len(A) + len(B))), ""]
    return "\n".join(texto)


def seccion_tfidf(comp, a, b):
    modelo = comp.tfidf
    tfa = frecuencias(preprocesar(a))
    tfb = frecuencias(preprocesar(b))
    va = modelo.vector(a)
    vb = modelo.vector(b)
    filas = []
    for p in tfa:
        if p in tfb:
            filas.append([p, tfa[p], tfb[p], modelo.df[p], "%.4f" % modelo.idf[p],
                          "%.4f" % va[p], "%.4f" % vb[p], "%.4f" % (va[p] * vb[p])])
    pp = producto_punto(va, vb)
    ma = magnitud(va)
    mb = magnitud(vb)
    cos = pp / (ma * mb)
    texto = ["## 4. TF-IDF + coseno", "",
             "N = %d abstracts. idf = log10(N / df). peso = tf · idf." % modelo.N, "",
             "Palabras comunes (las únicas que aportan al producto punto):", "",
             tabla_md(["palabra", "tf A", "tf B", "df", "idf", "peso A", "peso B", "A×B"], filas), "",
             "Producto punto A·B = %.4f" % pp,
             "|A| = raíz(%.4f) = %.4f   (%d palabras con peso)" % (ma * ma, ma, len(va)),
             "|B| = raíz(%.4f) = %.4f   (%d palabras con peso)" % (mb * mb, mb, len(vb)),
             "cos(θ) = %.4f / (%.4f · %.4f) = %.4f" % (pp, ma, mb, cos),
             "θ = %.2f grados" % math.degrees(math.acos(cos)), ""]
    return "\n".join(texto)


def seccion_ia(comp):
    texto = ["## 5 y 6. Modelos de IA (embeddings)", ""]
    for modelo in [comp.minilm, comp.glove]:
        va = modelo.vector(ID_A)
        vb = modelo.vector(ID_B)
        pp = producto_punto_listas(va, vb)
        ma = math.sqrt(producto_punto_listas(va, va))
        mb = math.sqrt(producto_punto_listas(vb, vb))
        texto += ["### " + modelo.descripcion,
                  "Dimensión del vector: %d" % len(va),
                  "Primeros 5 valores A: %s" % ", ".join("%.4f" % x for x in va[:5]),
                  "Primeros 5 valores B: %s" % ", ".join("%.4f" % x for x in vb[:5]),
                  "A·B = %.4f   |A| = %.4f   |B| = %.4f" % (pp, ma, mb),
                  "coseno = %.4f / (%.4f · %.4f) = %.4f" % (pp, ma, mb, pp / (ma * mb)),
                  "distancia euclidiana = %.4f" % modelo.distancia(ID_A, ID_B), ""]
    return "\n".join(texto)


def producto_punto_listas(a, b):
    suma = 0.0
    for k in range(len(a)):
        suma = suma + a[k] * b[k]
    return suma


def seccion_resumen(comp):
    res = comp.comparar_par(ID_A, ID_B)
    filas = []
    for alg in ALGORITMOS:
        valor, seg = res[alg]
        filas.append([alg, "%.4f" % valor, "%.4f s" % seg])
    return "\n".join(["## Resumen", "", tabla_md(["Algoritmo", "Similitud", "Tiempo"], filas), ""])


if __name__ == "__main__":
    comp = Comparador()
    a = comp.por_id[ID_A]["abstract"]
    b = comp.por_id[ID_B]["abstract"]
    partes = ["# Caso de estudio: artículo %d vs artículo %d" % (ID_A, ID_B), "",
              "A = " + comp.por_id[ID_A]["titulo"], "B = " + comp.por_id[ID_B]["titulo"], "",
              seccion_levenshtein(a, b), seccion_conjuntos(a, b), seccion_tfidf(comp, a, b),
              seccion_ia(comp), seccion_resumen(comp)]
    os.makedirs(CARPETA, exist_ok=True)
    ruta = os.path.join(CARPETA, "caso_estudio_11_vs_16.md")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(partes))
    print("Guardado en", ruta)
