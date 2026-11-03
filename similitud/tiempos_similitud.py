import os
import sys
import json
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from similitud.levenshtein import similitud_levenshtein
from similitud.jaccard import similitud_jaccard
from similitud.dice import similitud_dice
from similitud.tfidf_coseno import ModeloTFIDF

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(RAIZ, "salidas", "req1")
COLOR_A = "#0F5E6E"
COLOR_B = "#7A4FA3"
COLOR_C = "#E07A3F"
COLOR_D = "#2E9C8F"


def medir(funcion, repeticiones):
    """Mejor tiempo de varias repeticiones (el menos afectado por otros programas)."""
    mejor = None
    for r in range(repeticiones):
        inicio = time.perf_counter()
        funcion()
        t = time.perf_counter() - inicio
        if mejor is None or t < mejor:
            mejor = t
    return mejor


def experimento_levenshtein(a, b, tamanos):
    """Corto los dos abstracts al mismo largo n y mido: si es O(n·m) con n = m, el tiempo crece como n²."""
    filas = []
    for n in tamanos:
        t = medir(lambda: similitud_levenshtein(a[:n], b[:n]), 3)
        filas.append((n, (n + 1) * (n + 1), t))
        print("Levenshtein n =", n, "tiempo", round(t, 4))
    return filas


def experimento_lineales(a, b, abstracts, veces):
    """Repito el texto k veces: si el algoritmo es O(n), el tiempo crece en línea recta."""
    modelo = ModeloTFIDF(abstracts)
    filas = []
    for k in veces:
        ta = (a + " ") * k
        tb = (b + " ") * k
        fila = [len(ta)]
        fila.append(medir(lambda: similitud_jaccard(ta, tb), 5))
        fila.append(medir(lambda: similitud_dice(ta, tb), 5))
        fila.append(medir(lambda: modelo.similitud(ta, tb), 5))
        filas.append(fila)
        print("lineales n =", len(ta), [round(x, 5) for x in fila[1:]])
    return filas


def graficar(filas_lev, filas_lin, ruta):
    fig, ejes = plt.subplots(1, 3, figsize=(16, 4.8))
    ns = [f[0] for f in filas_lev]
    casillas = [f[1] / 1e6 for f in filas_lev]
    tiempos = [f[2] for f in filas_lev]
    ejes[0].plot(ns, tiempos, marker="o", color=COLOR_A)
    ejes[0].set_title("Levenshtein: tiempo contra n (n = m)")
    ejes[0].set_xlabel("n (letras de cada texto)")
    ejes[0].set_ylabel("segundos")
    ejes[1].plot(casillas, tiempos, marker="o", color=COLOR_A)
    ejes[1].set_title("Levenshtein: tiempo contra casillas (n+1)(m+1)")
    ejes[1].set_xlabel("casillas de la matriz (millones)")
    ejes[1].set_ylabel("segundos")
    largos = [f[0] for f in filas_lin]
    ejes[2].plot(largos, [f[1] * 1000 for f in filas_lin], marker="o", color=COLOR_B, label="Jaccard")
    ejes[2].plot(largos, [f[2] * 1000 for f in filas_lin], marker="o", color=COLOR_C, label="Dice")
    ejes[2].plot(largos, [f[3] * 1000 for f in filas_lin], marker="o", color=COLOR_D, label="TF-IDF + coseno")
    ejes[2].set_title("Jaccard, Dice y TF-IDF: tiempo contra n")
    ejes[2].set_xlabel("n (letras de cada texto)")
    ejes[2].set_ylabel("milisegundos")
    ejes[2].legend()
    for eje in ejes:
        eje.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    with open(os.path.join(RAIZ, "datos", "corpus.json"), encoding="utf-8") as f:
        corpus = json.load(f)
    abstracts = []
    for art in corpus:
        abstracts.append(art["abstract"])
    a = abstracts[11]   # artículo 12, de los más largos
    b = abstracts[4]    # artículo 5
    filas_lev = experimento_levenshtein(a, b, [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400])
    filas_lin = experimento_lineales(abstracts[10], abstracts[15], abstracts, [1, 2, 4, 6, 8, 10, 12, 14, 16])
    os.makedirs(CARPETA, exist_ok=True)
    graficar(filas_lev, filas_lin, os.path.join(CARPETA, "tiempos_similitud.png"))
    with open(os.path.join(CARPETA, "tiempos_similitud.csv"), "w", encoding="utf-8") as f:
        f.write("algoritmo,n,casillas_o_largo,segundos\n")
        for n, c, t in filas_lev:
            f.write("Levenshtein,%d,%d,%.6f\n" % (n, c, t))
        for fila in filas_lin:
            f.write("Jaccard,%d,%d,%.6f\n" % (fila[0], fila[0], fila[1]))
            f.write("Dice,%d,%d,%.6f\n" % (fila[0], fila[0], fila[2]))
            f.write("TF-IDF + coseno,%d,%d,%.6f\n" % (fila[0], fila[0], fila[3]))
