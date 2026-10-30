import os
import json
import math

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMBEDDINGS = os.path.join(RAIZ, "datos", "embeddings.json")


def cargar_embeddings(ruta=EMBEDDINGS):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def producto_punto(a, b):
    suma = 0.0
    for k in range(len(a)):
        suma = suma + a[k] * b[k]
    return suma


def magnitud(a):
    return math.sqrt(producto_punto(a, a))


def similitud_coseno(a, b):
    """cos = A·B / (|A| |B|)"""
    ma = magnitud(a)
    mb = magnitud(b)
    if ma == 0 or mb == 0:
        return 0.0
    return producto_punto(a, b) / (ma * mb)


def distancia_euclidiana(a, b):
    """raíz de la suma de (a_k - b_k)²"""
    suma = 0.0
    for k in range(len(a)):
        dif = a[k] - b[k]
        suma = suma + dif * dif
    return math.sqrt(suma)


def similitud_euclidiana(a, b):
    """Paso la distancia a similitud: 1 si son iguales, cerca de 0 si están lejos."""
    return 1 / (1 + distancia_euclidiana(a, b))


class ModeloIA:
    """Compara abstracts con los vectores ya calculados por un modelo preentrenado."""

    def __init__(self, nombre, embeddings=None):
        if embeddings is None:
            embeddings = cargar_embeddings()
        self.nombre = nombre
        self.descripcion = embeddings["modelos"][nombre]
        self.vectores = embeddings[nombre]

    def vector(self, id_articulo):
        return self.vectores[str(id_articulo)]

    def similitud(self, id_a, id_b):
        return similitud_coseno(self.vector(id_a), self.vector(id_b))

    def distancia(self, id_a, id_b):
        return distancia_euclidiana(self.vector(id_a), self.vector(id_b))


if __name__ == "__main__":
    emb = cargar_embeddings()
    for nombre in ["minilm", "glove"]:
        m = ModeloIA(nombre, emb)
        print(m.descripcion)
        print("  coseno 1 vs 2:", round(m.similitud(1, 2), 4), " euclidiana:", round(m.distancia(1, 2), 4))
