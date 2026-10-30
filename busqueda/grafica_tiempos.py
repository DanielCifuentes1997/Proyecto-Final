import os
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from busqueda.buscador import ALGORITMOS, minusculas, preprocesar_patron, buscar_en_texto
from similitud.comparar import cargar_corpus

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(RAIZ, "salidas", "req3")
COLORES = {"KMP": "#1f3a68", "Boyer-Moore": "#2e8b57", "Rabin-Karp": "#c0392b"}
REPETICIONES = 10


def tiempo_busqueda(algoritmo, texto, patron):
    tabla = preprocesar_patron(algoritmo, patron)
    inicio = time.perf_counter()
    for r in range(REPETICIONES):
        buscar_en_texto(algoritmo, texto, patron, tabla)
    return (time.perf_counter() - inicio) / REPETICIONES * 1000


def tiempo_preprocesamiento(algoritmo, patron):
    inicio = time.perf_counter()
    for r in range(REPETICIONES * 100):
        preprocesar_patron(algoritmo, patron)
    return (time.perf_counter() - inicio) / (REPETICIONES * 100) * 1000


def texto_completo():
    """Uno los 20 abstracts en un solo texto para poder ir creciendo n."""
    corpus, por_id = cargar_corpus()
    partes = []
    for art in corpus:
        partes.append(minusculas(art["abstract"]))
    return " ".join(partes)


def medir_contra_n(texto, patron):
    """Tiempo de búsqueda cuando el texto crece (el patrón queda fijo)."""
    tamanos = []
    tiempos = {}
    for alg in ALGORITMOS:
        tiempos[alg] = []
    paso = len(texto) // 10
    for k in range(1, 11):
        n = paso * k
        tamanos.append(n)
        for alg in ALGORITMOS:
            tiempos[alg].append(tiempo_busqueda(alg, texto[:n], patron))
    return tamanos, tiempos


def medir_contra_m(texto, patrones):
    """Tiempo de preprocesamiento y de búsqueda cuando el patrón crece (el texto queda fijo)."""
    largos = []
    pre = {}
    busq = {}
    for alg in ALGORITMOS:
        pre[alg] = []
        busq[alg] = []
    for patron in patrones:
        largos.append(len(patron))
        for alg in ALGORITMOS:
            pre[alg].append(tiempo_preprocesamiento(alg, patron))
            busq[alg].append(tiempo_busqueda(alg, texto, patron))
    return largos, pre, busq


def graficar(tamanos, tiempos_n, largos, pre_m, busq_m, ruta):
    fig, ejes = plt.subplots(1, 3, figsize=(16, 5))
    for alg in ALGORITMOS:
        ejes[0].plot(tamanos, tiempos_n[alg], marker="o", color=COLORES[alg], label=alg)
        ejes[1].plot(largos, busq_m[alg], marker="o", color=COLORES[alg], label=alg)
        ejes[2].plot(largos, pre_m[alg], marker="o", color=COLORES[alg], label=alg)
    ejes[0].set_title("Búsqueda vs tamaño del texto (patrón \"learning\")")
    ejes[0].set_xlabel("n (caracteres del texto)")
    ejes[0].set_ylabel("milisegundos")
    ejes[1].set_title("Búsqueda vs largo del patrón (n fijo)")
    ejes[1].set_xlabel("m (caracteres del patrón)")
    ejes[1].set_ylabel("milisegundos")
    ejes[2].set_title("Preprocesamiento vs largo del patrón")
    ejes[2].set_xlabel("m (caracteres del patrón)")
    ejes[2].set_ylabel("milisegundos")
    for eje in ejes:
        eje.legend()
        eje.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    texto = texto_completo()
    patrones = ["ai", "data", "learning", "assessment", "higher education", "artificial intelligence",
                "generative artificial intelligence"]
    tamanos, tiempos_n = medir_contra_n(texto, "learning")
    largos, pre_m, busq_m = medir_contra_m(texto, patrones)
    os.makedirs(CARPETA, exist_ok=True)
    graficar(tamanos, tiempos_n, largos, pre_m, busq_m, os.path.join(CARPETA, "tiempos_busqueda.png"))
    with open(os.path.join(CARPETA, "tiempos.csv"), "w", encoding="utf-8") as f:
        f.write("patron,m,algoritmo,preprocesamiento_ms,busqueda_ms\n")
        for i in range(len(patrones)):
            for alg in ALGORITMOS:
                f.write("%s,%d,%s,%.6f,%.4f\n" % (patrones[i], largos[i], alg, pre_m[alg][i], busq_m[alg][i]))
    print("n total del texto:", len(texto))
    for i in range(len(patrones)):
        linea = "m=%2d %-35s" % (largos[i], patrones[i])
        for alg in ALGORITMOS:
            linea = linea + "  %s pre=%.4f busq=%.2f" % (alg[:3], pre_m[alg][i], busq_m[alg][i])
        print(linea)
