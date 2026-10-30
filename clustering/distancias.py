import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from similitud.tfidf_coseno import ModeloTFIDF, coseno


def matriz_distancias(abstracts):
    """Distancia entre cada par de abstracts: 1 - coseno de sus vectores TF-IDF."""
    modelo = ModeloTFIDF(abstracts)
    vectores = []
    for i in range(len(abstracts)):
        vectores.append(modelo.vector(abstracts[i]))
    n = len(abstracts)
    D = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(0.0)
        D.append(fila)
    # la matriz es simétrica, calculo solo la mitad de arriba
    for i in range(n):
        for j in range(i + 1, n):
            d = 1 - coseno(vectores[i], vectores[j])
            D[i][j] = d
            D[j][i] = d
    return D
