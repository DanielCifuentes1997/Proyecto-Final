import os
import sys
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocesamiento.texto import tokenizar, preprocesar
from similitud.tfidf_coseno import frecuencia_documental, calcular_idf

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(RAIZ, "datos", "corpus.json")
CARPETA = os.path.join(RAIZ, "salidas", "corpus")
COLOR = "#0F5E6E"


def estadisticas(corpus):
    """Palabras, palabras limpias y términos distintos de cada abstract."""
    filas = []
    for art in corpus:
        tokens = tokenizar(art["abstract"])
        limpias = preprocesar(art["abstract"])
        distintas = {}
        for p in limpias:
            distintas[p] = True
        filas.append({"id": art["id"], "caracteres": len(art["abstract"]), "palabras": len(tokens),
                      "limpias": len(limpias), "distintas": len(distintas), "autores": len(art["autores"])})
    return filas


def palabras_mas_repartidas(corpus, cuantas=15):
    """Las palabras que aparecen en más abstracts (df alto = idf bajo)."""
    tokens = []
    for art in corpus:
        tokens.append(preprocesar(art["abstract"]))
    df = frecuencia_documental(tokens)
    idf = calcular_idf(df, len(corpus))
    lista = []
    for palabra in df:
        lista.append((df[palabra], palabra))
    lista.sort(reverse=True)
    salida = []
    for k in range(cuantas):
        salida.append({"palabra": lista[k][1], "df": lista[k][0], "idf": idf[lista[k][1]]})
    return salida, df


def graficar_largos(filas, ruta):
    ids = []
    palabras = []
    for f in filas:
        ids.append(str(f["id"]))
        palabras.append(f["palabras"])
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(ids, palabras, color=COLOR)
    for k in range(len(ids)):
        ax.text(k, palabras[k] + 3, str(palabras[k]), ha="center", fontsize=8)
    ax.set_xlabel("Artículo")
    ax.set_ylabel("Palabras del abstract")
    ax.set_title("Largo de cada abstract")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def graficar_repartidas(lista, n, ruta):
    palabras = []
    dfs = []
    for item in lista:
        palabras.append(item["palabra"])
        dfs.append(item["df"])
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.barh(palabras[::-1], dfs[::-1], color=COLOR)
    for k in range(len(lista)):
        item = lista[len(lista) - 1 - k]
        ax.text(item["df"] + 0.2, k, "df = %d   idf = %.3f" % (item["df"], item["idf"]), va="center", fontsize=8)
    ax.set_xlim(0, n + 6)
    ax.set_xlabel("En cuántos abstracts aparece (df)")
    ax.set_title("Las palabras que aparecen en más abstracts")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    with open(CORPUS, encoding="utf-8") as f:
        corpus = json.load(f)
    os.makedirs(CARPETA, exist_ok=True)
    filas = estadisticas(corpus)
    lista, df = palabras_mas_repartidas(corpus)
    graficar_largos(filas, os.path.join(CARPETA, "largo_abstracts.png"))
    graficar_repartidas(lista, len(corpus), os.path.join(CARPETA, "palabras_mas_repartidas.png"))
    with open(os.path.join(CARPETA, "estadisticas.csv"), "w", encoding="utf-8") as f:
        f.write("id,caracteres,palabras,palabras_limpias,terminos_distintos,autores\n")
        for e in filas:
            f.write("%d,%d,%d,%d,%d,%d\n" % (e["id"], e["caracteres"], e["palabras"], e["limpias"], e["distintas"], e["autores"]))
    for e in filas:
        print(e)
    print("Vocabulario:", len(df))
    for item in lista:
        print(item)
