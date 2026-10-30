import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocesamiento.texto import preprocesar


def frecuencias(palabras):
    """TF: cuántas veces aparece cada palabra."""
    tf = {}
    for i in range(len(palabras)):
        p = palabras[i]
        if p in tf:
            tf[p] = tf[p] + 1
        else:
            tf[p] = 1
    return tf


def frecuencia_documental(corpus_tokens):
    """df: en cuántos abstracts aparece cada palabra."""
    df = {}
    for d in range(len(corpus_tokens)):
        vistas = {}
        palabras = corpus_tokens[d]
        for i in range(len(palabras)):
            p = palabras[i]
            # cada abstract cuenta una sola vez
            if p not in vistas:
                vistas[p] = True
                if p in df:
                    df[p] = df[p] + 1
                else:
                    df[p] = 1
    return df


def calcular_idf(df, N):
    """idf = log10(N / df)"""
    idf = {}
    for palabra in df:
        idf[palabra] = math.log10(N / df[palabra])
    return idf


def vector_tfidf(palabras, idf):
    """peso = tf * idf"""
    tf = frecuencias(palabras)
    vector = {}
    for palabra in tf:
        vector[palabra] = tf[palabra] * idf.get(palabra, 0.0)
    return vector


def producto_punto(v1, v2):
    suma = 0.0
    for palabra in v1:
        if palabra in v2:
            suma = suma + v1[palabra] * v2[palabra]
    return suma


def magnitud(v):
    suma = 0.0
    for palabra in v:
        suma = suma + v[palabra] * v[palabra]
    return math.sqrt(suma)


def coseno(v1, v2):
    """cos = A·B / (|A| |B|)"""
    m1 = magnitud(v1)
    m2 = magnitud(v2)
    if m1 == 0 or m2 == 0:
        return 0.0
    return producto_punto(v1, v2) / (m1 * m2)


class ModeloTFIDF:
    """Calcula el idf una vez con los 20 abstracts y después compara los que quiera."""

    def __init__(self, abstracts):
        self.tokens = []
        for i in range(len(abstracts)):
            self.tokens.append(preprocesar(abstracts[i]))
        self.N = len(abstracts)
        self.df = frecuencia_documental(self.tokens)
        self.idf = calcular_idf(self.df, self.N)

    def vector(self, texto):
        return vector_tfidf(preprocesar(texto), self.idf)

    def similitud(self, texto_a, texto_b):
        return coseno(self.vector(texto_a), self.vector(texto_b))


if __name__ == "__main__":
    import json
    ruta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "datos", "corpus.json")
    corpus = json.load(open(ruta, encoding="utf-8"))
    abstracts = [art["abstract"] for art in corpus]
    modelo = ModeloTFIDF(abstracts)
    for p in ["artificial", "intelligence", "ai", "learning", "assessment", "stem"]:
        print(p, "df =", modelo.df[p], "idf =", round(modelo.idf[p], 4))
    print("Artículo 1 vs 2:", round(modelo.similitud(abstracts[0], abstracts[1]), 4))
