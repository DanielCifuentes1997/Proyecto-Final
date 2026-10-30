import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from similitud.levenshtein import similitud_levenshtein
from similitud.jaccard import similitud_jaccard
from similitud.dice import similitud_dice
from similitud.tfidf_coseno import ModeloTFIDF
from similitud.ia_embeddings import ModeloIA, cargar_embeddings

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(RAIZ, "datos", "corpus.json")

ALGORITMOS = ["Levenshtein", "Jaccard", "Dice", "TF-IDF + coseno", "MiniLM (IA)", "GloVe (IA)"]


def cargar_corpus(ruta=CORPUS):
    with open(ruta, encoding="utf-8") as f:
        corpus = json.load(f)
    por_id = {}
    for art in corpus:
        por_id[art["id"]] = art
    return corpus, por_id


class Comparador:
    """Carga todo una vez y compara los artículos que se elijan con los 6 algoritmos."""

    def __init__(self):
        self.corpus, self.por_id = cargar_corpus()
        abstracts = []
        for art in self.corpus:
            abstracts.append(art["abstract"])
        self.tfidf = ModeloTFIDF(abstracts)
        embeddings = cargar_embeddings()
        self.minilm = ModeloIA("minilm", embeddings)
        self.glove = ModeloIA("glove", embeddings)

    def comparar_par(self, id_a, id_b):
        """Devuelve {algoritmo: (similitud, segundos)} para un par de artículos."""
        a = self.por_id[id_a]["abstract"]
        b = self.por_id[id_b]["abstract"]
        funciones = [
            lambda: similitud_levenshtein(a, b),
            lambda: similitud_jaccard(a, b),
            lambda: similitud_dice(a, b),
            lambda: self.tfidf.similitud(a, b),
            lambda: self.minilm.similitud(id_a, id_b),
            lambda: self.glove.similitud(id_a, id_b),
        ]
        resultado = {}
        for k in range(len(ALGORITMOS)):
            inicio = time.perf_counter()
            valor = funciones[k]()
            resultado[ALGORITMOS[k]] = (valor, time.perf_counter() - inicio)
        return resultado

    def comparar_varios(self, ids):
        """Compara todos contra todos: con n artículos salen n(n-1)/2 pares."""
        filas = []
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                filas.append((ids[i], ids[j], self.comparar_par(ids[i], ids[j])))
        return filas


if __name__ == "__main__":
    ids = [11, 16]
    if len(sys.argv) > 1:
        ids = [int(x) for x in sys.argv[1].split(",")]
    comp = Comparador()
    for id_a, id_b, res in comp.comparar_varios(ids):
        print("Artículo", id_a, "vs", id_b)
        for alg in ALGORITMOS:
            valor, seg = res[alg]
            print("  %-16s %.4f   (%.4f s)" % (alg, valor, seg))
