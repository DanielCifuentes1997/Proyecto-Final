import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocesamiento.texto import a_minuscula
from similitud.comparar import cargar_corpus
from busqueda.kmp import tabla_prefijos, buscar_kmp
from busqueda.boyer_moore import tabla_caracter_malo, buscar_boyer_moore
from busqueda.rabin_karp import preparar_patron, buscar_rabin_karp

ALGORITMOS = ["KMP", "Boyer-Moore", "Rabin-Karp"]


def minusculas(texto):
    """Para que 'Learning' y 'learning' se encuentren igual."""
    resultado = []
    for i in range(len(texto)):
        resultado.append(a_minuscula(texto[i]))
    return "".join(resultado)


def preprocesar_patron(algoritmo, patron):
    if algoritmo == "KMP":
        return tabla_prefijos(patron)
    if algoritmo == "Boyer-Moore":
        return tabla_caracter_malo(patron)
    return preparar_patron(patron)


def buscar_en_texto(algoritmo, texto, patron, tabla):
    if algoritmo == "KMP":
        return buscar_kmp(texto, patron, tabla), 0
    if algoritmo == "Boyer-Moore":
        return buscar_boyer_moore(texto, patron, tabla), 0
    return buscar_rabin_karp(texto, patron, tabla)


class Buscador:
    """Busca un patrón en los 20 abstracts con los 3 algoritmos y mide los tiempos."""

    def __init__(self):
        self.corpus, self.por_id = cargar_corpus()
        self.textos = {}
        for art in self.corpus:
            self.textos[art["id"]] = minusculas(art["abstract"])

    def buscar(self, patron, repeticiones=20):
        patron = minusculas(patron)
        resultados = {}
        for algoritmo in ALGORITMOS:
            # preprocesamiento: se hace una sola vez por patrón
            inicio = time.perf_counter()
            for r in range(repeticiones):
                tabla = preprocesar_patron(algoritmo, patron)
            t_pre = (time.perf_counter() - inicio) / repeticiones
            # búsqueda en los 20 abstracts
            inicio = time.perf_counter()
            for r in range(repeticiones):
                encontrados = {}
                colisiones = 0
                for id_art in self.textos:
                    posiciones, col = buscar_en_texto(algoritmo, self.textos[id_art], patron, tabla)
                    colisiones = colisiones + col
                    if len(posiciones) > 0:
                        encontrados[id_art] = posiciones
            t_busq = (time.perf_counter() - inicio) / repeticiones
            total = 0
            for id_art in encontrados:
                total = total + len(encontrados[id_art])
            resultados[algoritmo] = {"encontrados": encontrados, "ocurrencias": total, "colisiones": colisiones,
                                     "t_preprocesamiento": t_pre, "t_busqueda": t_busq}
        return resultados


def fragmento(texto, posicion, largo_patron, contexto=40):
    """Un pedacito del abstract alrededor de la ocurrencia, para mostrarla."""
    inicio = posicion - contexto
    if inicio < 0:
        inicio = 0
    fin = posicion + largo_patron + contexto
    if fin > len(texto):
        fin = len(texto)
    return "..." + texto[inicio:posicion] + "[" + texto[posicion:posicion + largo_patron] + "]" + texto[posicion + largo_patron:fin] + "..."


if __name__ == "__main__":
    patron = "learning"
    if len(sys.argv) > 1:
        patron = sys.argv[1]
    b = Buscador()
    res = b.buscar(patron)
    for alg in ALGORITMOS:
        r = res[alg]
        print("%-12s ocurrencias=%d en %d abstracts  colisiones=%d  preproc=%.6f ms  búsqueda=%.4f ms" % (
            alg, r["ocurrencias"], len(r["encontrados"]), r["colisiones"],
            r["t_preprocesamiento"] * 1000, r["t_busqueda"] * 1000))
    primero = res["KMP"]["encontrados"]
    for id_art in primero:
        texto = b.textos[id_art]
        print("Art.", id_art, fragmento(texto, primero[id_art][0], len(patron)))
        break
