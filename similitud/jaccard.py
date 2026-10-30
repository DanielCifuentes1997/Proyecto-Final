"""
Coeficiente de Jaccard.

Compara el VOCABULARIO de dos textos: qué palabras distintas comparten.

    J(A, B) = |A ∩ B| / |A ∪ B|

    A ∩ B (intersección) = palabras que están en los dos textos
    A ∪ B (unión)        = palabras que están en al menos uno de los textos
    |X|                  = cantidad de palabras distintas de X

Como la unión cuenta dos veces las palabras comunes:  |A ∪ B| = |A| + |B| - |A ∩ B|

Los conjuntos se guardan en un diccionario (palabra -> True):
buscar si una palabra está en el diccionario toma tiempo constante.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocesamiento.texto import preprocesar


def conjunto(palabras):
    """Lista de palabras -> diccionario con cada palabra UNA sola vez (sin repetidas)."""
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
    A = conjunto(preprocesar(a))
    B = conjunto(preprocesar(b))
    print("A:", list(A), len(A))
    print("B:", list(B), len(B))
    print("Comunes:", [p for p in A if p in B])
    print("Jaccard:", round(similitud_jaccard(a, b), 4))
