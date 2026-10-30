import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocesamiento.texto import preprocesar


def conjunto(palabras):
    """Deja cada palabra una sola vez."""
    c = {}
    for i in range(len(palabras)):
        c[palabras[i]] = True
    return c


def tamano_interseccion(c1, c2):
    """Cuenta cuántas palabras de c1 también están en c2."""
    comunes = 0
    for palabra in c1:
        if palabra in c2:
            comunes = comunes + 1
    return comunes


def similitud_jaccard(texto_a, texto_b):
    A = conjunto(preprocesar(texto_a))
    B = conjunto(preprocesar(texto_b))
    interseccion = tamano_interseccion(A, B)
    union = len(A) + len(B) - interseccion
    if union == 0:
        return 0.0
    return interseccion / union


if __name__ == "__main__":
    a = ("The field of education has experienced a transformation as artificial intelligence (AI) "
         "becomes increasingly applicable for learning purposes")
    b = ("Artificial intelligence (AI), as an emerging technology, has been widely used in STEM "
         "education to promote the educational assessment")
    print("Jaccard:", round(similitud_jaccard(a, b), 4))
