import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocesamiento.texto import preprocesar

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(RAIZ, "datos", "corpus.json")
SALIDA = os.path.join(RAIZ, "datos", "embeddings.json")

MODELO_FRASES = "all-MiniLM-L6-v2"
MODELO_PALABRAS = "glove-wiki-gigaword-100"


def embedding_frases(modelo, texto):
    """El modelo lee el abstract completo y devuelve un solo vector."""
    vector = modelo.encode(texto)
    return [float(x) for x in vector]


def embedding_promedio_palabras(vectores_palabras, texto):
    """Promedio de los vectores GloVe de las palabras del abstract."""
    palabras = preprocesar(texto)
    dimension = vectores_palabras.vector_size
    suma = [0.0] * dimension
    usadas = 0
    for i in range(len(palabras)):
        p = palabras[i]
        # si el modelo no conoce la palabra la salto
        if p in vectores_palabras.key_to_index:
            v = vectores_palabras[p]
            for k in range(dimension):
                suma[k] = suma[k] + float(v[k])
            usadas = usadas + 1
    if usadas == 0:
        return suma, 0, len(palabras)
    promedio = []
    for k in range(dimension):
        promedio.append(suma[k] / usadas)
    return promedio, usadas, len(palabras)


def redondear(vector):
    return [round(x, 6) for x in vector]


if __name__ == "__main__":
    from sentence_transformers import SentenceTransformer
    import gensim.downloader

    corpus = json.load(open(CORPUS, encoding="utf-8"))
    modelo_frases = SentenceTransformer(MODELO_FRASES)
    vectores_palabras = gensim.downloader.load(MODELO_PALABRAS)

    resultado = {
        "modelos": {
            "minilm": MODELO_FRASES + " (sentence-transformers, 384 dimensiones)",
            "glove": MODELO_PALABRAS + " (promedio de vectores de palabras, 100 dimensiones)",
        },
        "minilm": {},
        "glove": {},
    }
    for art in corpus:
        clave = str(art["id"])
        resultado["minilm"][clave] = redondear(embedding_frases(modelo_frases, art["abstract"]))
        promedio, usadas, total = embedding_promedio_palabras(vectores_palabras, art["abstract"])
        resultado["glove"][clave] = redondear(promedio)
        print("Artículo", clave, "- GloVe conoce", usadas, "de", total, "palabras")

    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(resultado, f)
    print("Embeddings guardados en", SALIDA)
