import os
import sys
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from similitud.comparar import Comparador, ALGORITMOS
from clustering.metrica import correlacion_pearson

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(RAIZ, "salidas", "req1")
ARCHIVO = os.path.join(CARPETA, "todos_los_pares.csv")
COLOR_CLASICO = "#0F5E6E"
COLOR_IA = "#7A4FA3"


def calcular_todos(comp):
    """Compara cada par del corpus (n(n-1)/2 pares) con los 6 algoritmos."""
    ids = []
    for art in comp.corpus:
        ids.append(art["id"])
    filas = []
    total = len(ids) * (len(ids) - 1) // 2
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            res = comp.comparar_par(ids[i], ids[j])
            fila = {"a": ids[i], "b": ids[j]}
            for alg in ALGORITMOS:
                fila[alg] = res[alg][0]
                fila["t " + alg] = res[alg][1]
            filas.append(fila)
            print("par", len(filas), "de", total)
    return filas


def guardar_csv(filas, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("a,b," + ",".join(ALGORITMOS) + "," + ",".join("t " + alg for alg in ALGORITMOS) + "\n")
        for fila in filas:
            valores = [str(fila["a"]), str(fila["b"])]
            for alg in ALGORITMOS:
                valores.append("%.6f" % fila[alg])
            for alg in ALGORITMOS:
                valores.append("%.6f" % fila["t " + alg])
            f.write(",".join(valores) + "\n")


def leer_csv(ruta):
    filas = []
    with open(ruta, encoding="utf-8") as f:
        encabezado = f.readline().strip().split(",")
        for linea in f:
            partes = linea.strip().split(",")
            fila = {"a": int(partes[0]), "b": int(partes[1])}
            for k in range(2, len(partes)):
                fila[encabezado[k]] = float(partes[k])
            filas.append(fila)
    return filas


def resumen(filas):
    """Promedio, mínimo, máximo y desviación de cada algoritmo sobre todos los pares."""
    salida = {}
    for alg in ALGORITMOS:
        valores = []
        tiempos = 0.0
        for fila in filas:
            valores.append(fila[alg])
            tiempos = tiempos + fila["t " + alg]
        n = len(valores)
        promedio = 0.0
        minimo = valores[0]
        maximo = valores[0]
        par_max = (filas[0]["a"], filas[0]["b"])
        for k in range(n):
            promedio = promedio + valores[k]
            if valores[k] < minimo:
                minimo = valores[k]
            if valores[k] > maximo:
                maximo = valores[k]
                par_max = (filas[k]["a"], filas[k]["b"])
        promedio = promedio / n
        suma = 0.0
        for k in range(n):
            suma = suma + (valores[k] - promedio) ** 2
        salida[alg] = {"promedio": promedio, "minimo": minimo, "maximo": maximo, "par_maximo": par_max,
                       "desviacion": math.sqrt(suma / n), "tiempo_promedio": tiempos / n}
    return salida


def matriz_correlaciones(filas):
    """Qué tanto se parecen las respuestas de cada par de algoritmos (correlación de Pearson)."""
    columnas = {}
    for alg in ALGORITMOS:
        columnas[alg] = []
        for fila in filas:
            columnas[alg].append(fila[alg])
    M = []
    for x in ALGORITMOS:
        fila = []
        for y in ALGORITMOS:
            fila.append(correlacion_pearson(columnas[x], columnas[y]))
        M.append(fila)
    return M


def graficar_distribucion(filas, ruta):
    datos = []
    for alg in ALGORITMOS:
        valores = []
        for fila in filas:
            valores.append(fila[alg])
        datos.append(valores)
    fig, ax = plt.subplots(figsize=(10, 4.8))
    cajas = ax.boxplot(datos, patch_artist=True, widths=0.55)
    for k in range(len(ALGORITMOS)):
        color = COLOR_IA if "IA" in ALGORITMOS[k] else COLOR_CLASICO
        cajas["boxes"][k].set_facecolor(color)
        cajas["boxes"][k].set_alpha(0.35)
        cajas["boxes"][k].set_edgecolor(color)
        cajas["medians"][k].set_color("black")
    ax.set_xticks(range(1, len(ALGORITMOS) + 1))
    ax.set_xticklabels(ALGORITMOS)
    ax.set_ylabel("Similitud")
    ax.set_ylim(0, 1.05)
    ax.set_title("Similitud de los %d pares de artículos según cada algoritmo" % len(filas))
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def graficar_correlaciones(M, ruta):
    fig, ax = plt.subplots(figsize=(7.5, 6))
    imagen = ax.imshow(M, cmap="BuGn", vmin=0, vmax=1)
    for i in range(len(M)):
        for j in range(len(M)):
            color = "white" if M[i][j] > 0.65 else "black"
            ax.text(j, i, "%.2f" % M[i][j], ha="center", va="center", color=color, fontsize=10)
    ax.set_xticks(range(len(ALGORITMOS)))
    ax.set_xticklabels(ALGORITMOS, rotation=30, ha="right")
    ax.set_yticks(range(len(ALGORITMOS)))
    ax.set_yticklabels(ALGORITMOS)
    ax.set_title("Correlación entre los algoritmos (190 pares)")
    fig.colorbar(imagen, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def graficar_dispersion(filas, ruta):
    """Cada punto es un par: TF-IDF (clásico) contra MiniLM (IA)."""
    xs = []
    ys = []
    for fila in filas:
        xs.append(fila["TF-IDF + coseno"])
        ys.append(fila["MiniLM (IA)"])
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    ax.scatter(xs, ys, s=22, color=COLOR_CLASICO, alpha=0.7)
    # marco el caso de estudio (11 y 16) y el par 2 y 6
    for fila in filas:
        if (fila["a"], fila["b"]) in [(11, 16), (2, 6)]:
            ax.scatter([fila["TF-IDF + coseno"]], [fila["MiniLM (IA)"]], s=70, color=COLOR_IA)
            ax.annotate("%d y %d" % (fila["a"], fila["b"]), (fila["TF-IDF + coseno"], fila["MiniLM (IA)"]),
                        textcoords="offset points", xytext=(6, 6))
    ax.set_xlabel("Similitud TF-IDF + coseno (clásico)")
    ax.set_ylabel("Similitud MiniLM (IA)")
    ax.set_title("Cada punto es un par de artículos")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(CARPETA, exist_ok=True)
    if os.path.exists(ARCHIVO) and "--recalcular" not in sys.argv:
        filas = leer_csv(ARCHIVO)
    else:
        filas = calcular_todos(Comparador())
        guardar_csv(filas, ARCHIVO)
    datos = resumen(filas)
    M = matriz_correlaciones(filas)
    graficar_distribucion(filas, os.path.join(CARPETA, "distribucion_pares.png"))
    graficar_correlaciones(M, os.path.join(CARPETA, "correlacion_algoritmos.png"))
    graficar_dispersion(filas, os.path.join(CARPETA, "tfidf_vs_minilm.png"))
    for alg in ALGORITMOS:
        r = datos[alg]
        print("%-16s promedio %.4f  mín %.4f  máx %.4f (par %s)  desv %.4f  tiempo %.5f s" % (
            alg, r["promedio"], r["minimo"], r["maximo"], r["par_maximo"], r["desviacion"], r["tiempo_promedio"]))
