"""
Similitud del coseno usando pesos TF-IDF.

1) TF (frecuencia del término): cuántas veces aparece la palabra t en el abstract d.
       tf(t, d) = número de veces que t aparece en d
2) IDF (frecuencia inversa en documentos): qué tan rara es la palabra en el corpus.
       idf(t) = log10( N / df(t) )
       N     = número de abstracts del corpus (20)
       df(t) = en cuántos abstracts aparece t
   Si una palabra está en los 20 abstracts: idf = log10(20/20) = 0 -> no sirve para diferenciar.
3) Peso TF-IDF:   w(t, d) = tf(t, d) · idf(t)
   Cada abstract queda como un vector de pesos (una posición por palabra).
4) Coseno del ángulo entre los dos vectores:
       cos(θ) = (A · B) / (|A| · |B|)
       A · B = suma de w(t, A) · w(t, B)          (producto punto)
       |A|   = raíz( suma de w(t, A)² )           (magnitud o norma)
   1 = mismo sentido (muy parecidos), 0 = perpendiculares (nada en común).

Los vectores se guardan en diccionarios (palabra -> peso) para no guardar los ceros.
Solo se usan log10 y sqrt de la librería math (operaciones matemáticas básicas).
"""
import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocesamiento.texto import preprocesar


def frecuencias(palabras):
    """TF: diccionario palabra -> cuántas veces aparece en la lista."""
    tf = {}
    for i in range(len(palabras)):
        p = palabras[i]
        if p in tf:
            tf[p] = tf[p] + 1
        else:
            tf[p] = 1
    return tf


def frecuencia_documental(corpus_tokens):
    """df: diccionario palabra -> en cuántos documentos aparece (cada documento cuenta una vez)."""
    df = {}
    for d in range(len(corpus_tokens)):
        vistas = {}
        palabras = corpus_tokens[d]
        for i in range(len(palabras)):
            p = palabras[i]
            if p not in vistas:
                vistas[p] = True
                if p in df:
                    df[p] = df[p] + 1
                else:
                    df[p] = 1
    return df


def calcular_idf(df, N):
    """idf(t) = log10(N / df(t)) para cada palabra del corpus."""
    idf = {}
    for palabra in df:
        idf[palabra] = math.log10(N / df[palabra])
    return idf


def vector_tfidf(palabras, idf):
    """Vector del documento: palabra -> tf · idf."""
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
    m1 = magnitud(v1)
    m2 = magnitud(v2)
    if m1 == 0 or m2 == 0:
        return 0.0
    return producto_punto(v1, v2) / (m1 * m2)


class ModeloTFIDF:
    """Calcula el IDF una sola vez con los abstracts del corpus y luego compara pares."""

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
    print("N =", modelo.N, " palabras distintas en el corpus:", len(modelo.df))
    for p in ["artificial", "intelligence", "ai", "education", "learning", "assessment", "stem", "transformation"]:
        print("%-15s df=%2d  idf=log10(20/%d)=%.4f" % (p, modelo.df[p], modelo.df[p], modelo.idf[p]))
    print("Artículo 1 vs 2:", round(modelo.similitud(abstracts[0], abstracts[1]), 4))
