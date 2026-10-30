import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from similitud.comparar import Comparador, ALGORITMOS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(RAIZ, "salidas", "req1")
COLOR_CLASICO = "#1f3a68"
COLOR_IA = "#2e8b57"


def figura_comparacion(resultado, titulo):
    """Barras con la similitud de cada algoritmo para un par de artículos (azul = clásicos, verde = IA)."""
    valores = []
    colores = []
    for alg in ALGORITMOS:
        valores.append(resultado[alg][0])
        if "IA" in alg:
            colores.append(COLOR_IA)
        else:
            colores.append(COLOR_CLASICO)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    barras = ax.bar(ALGORITMOS, valores, color=colores)
    # escribo el valor encima de cada barra
    for k in range(len(barras)):
        ax.text(barras[k].get_x() + barras[k].get_width() / 2, valores[k] + 0.02, "%.4f" % valores[k],
                ha="center", fontsize=9)
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Similitud (0 = distintos, 1 = iguales)")
    ax.set_title(titulo)
    ax.tick_params(axis="x", labelrotation=15)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    comp = Comparador()
    id_a, id_b = 11, 16
    resultado = comp.comparar_par(id_a, id_b)
    fig = figura_comparacion(resultado, "Similitud entre el artículo %d y el artículo %d" % (id_a, id_b))
    os.makedirs(CARPETA, exist_ok=True)
    ruta = os.path.join(CARPETA, "similitud_11_vs_16.png")
    fig.savefig(ruta, dpi=150)
    print("Guardada en", ruta)
