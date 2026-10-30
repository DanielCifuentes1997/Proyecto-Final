"""
Coeficiente de Dice (Sørensen–Dice).

Igual que Jaccard compara el vocabulario de dos textos, pero divide de otra forma:

    D(A, B) = 2 · |A ∩ B| / (|A| + |B|)

Las palabras comunes se cuentan dos veces arriba (una por cada texto)
y abajo se suman los tamaños de los dos conjuntos.
Reutiliza las funciones de conjuntos de jaccard.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocesamiento.texto import preprocesar
from similitud.jaccard import conjunto, tamano_interseccion


def similitud_dice(texto_a, texto_b):
    A = conjunto(preprocesar(texto_a))
    B = conjunto(preprocesar(texto_b))
    total = len(A) + len(B)
    if total == 0:
        return 0.0
    return 2 * tamano_interseccion(A, B) / total


if __name__ == "__main__":
    a = ("The field of education has experienced a transformation as artificial intelligence (AI) "
         "becomes increasingly applicable for learning purposes")
    b = ("Artificial intelligence (AI), as an emerging technology, has been widely used in STEM "
         "education to promote the educational assessment")
    print("Dice:", round(similitud_dice(a, b), 4))
