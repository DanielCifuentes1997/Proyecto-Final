"""
Distancia de Levenshtein (distancia de edición) con programación dinámica.

La distancia entre dos textos A y B es el número MÍNIMO de operaciones
(insertar, borrar o cambiar una letra) para convertir A en B.

Se llena una matriz D de (n + 1) x (m + 1), igual que la tabulación (Bottom Up)
del Núcleo 5: cada casilla se calcula con casillas que ya se llenaron antes.

    D[i][0] = i                     (borrar las i primeras letras de A)
    D[0][j] = j                     (insertar las j primeras letras de B)
    D[i][j] = mínimo de:
        D[i-1][j]   + 1             (borrar)
        D[i][j-1]   + 1             (insertar)
        D[i-1][j-1] + costo         (cambiar; costo = 0 si las letras son iguales, 1 si no)

La distancia es la última casilla D[n][m].
Similitud = 1 - distancia / max(n, m)   (1 = textos iguales, 0 = totalmente distintos)
"""


def minimo(a, b, c):
    """El menor de tres números."""
    menor = a
    if b < menor:
        menor = b
    if c < menor:
        menor = c
    return menor


def matriz_levenshtein(a, b):
    """Construye y devuelve la matriz D completa."""
    n = len(a)
    m = len(b)
    # matriz de (n + 1) filas y (m + 1) columnas llena de ceros
    D = []
    for i in range(n + 1):
        fila = []
        for j in range(m + 1):
            fila.append(0)
        D.append(fila)
    # casos base: primera columna y primera fila
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    # llenado de la tabla, fila por fila
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                costo = 0
            else:
                costo = 1
            D[i][j] = minimo(D[i - 1][j] + 1,           # borrar
                             D[i][j - 1] + 1,           # insertar
                             D[i - 1][j - 1] + costo)   # cambiar (o dejar igual)
    return D


def distancia_levenshtein(a, b):
    D = matriz_levenshtein(a, b)
    return D[len(a)][len(b)]


def similitud_levenshtein(a, b):
    """Convierte la distancia en una similitud entre 0 y 1."""
    if len(a) == 0 and len(b) == 0:
        return 1.0
    mayor = len(a)
    if len(b) > mayor:
        mayor = len(b)
    return 1 - distancia_levenshtein(a, b) / mayor


if __name__ == "__main__":
    a, b = "learning", "teaching"
    D = matriz_levenshtein(a, b)
    print("     ", "  ".join(" " + b))
    for i in range(len(a) + 1):
        letra = " " if i == 0 else a[i - 1]
        print(letra, " ".join("%2d" % v for v in D[i]))
    print("Distancia:", distancia_levenshtein(a, b))
    print("Similitud:", round(similitud_levenshtein(a, b), 4))
