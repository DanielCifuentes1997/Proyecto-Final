def minimo(a, b, c):
    menor = a
    if b < menor:
        menor = b
    if c < menor:
        menor = c
    return menor


def matriz_levenshtein(a, b):
    n = len(a)
    m = len(b)
    D = []
    for i in range(n + 1):
        fila = []
        for j in range(m + 1):
            fila.append(0)
        D.append(fila)
    # casos base
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    # lleno la tabla con borrar, insertar o cambiar
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                costo = 0
            else:
                costo = 1
            D[i][j] = minimo(D[i - 1][j] + 1,
                             D[i][j - 1] + 1,
                             D[i - 1][j - 1] + costo)
    return D


def distancia_levenshtein(a, b):
    D = matriz_levenshtein(a, b)
    return D[len(a)][len(b)]


def similitud_levenshtein(a, b):
    """1 - distancia / longitud del texto más largo."""
    if len(a) == 0 and len(b) == 0:
        return 1.0
    mayor = len(a)
    if len(b) > mayor:
        mayor = len(b)
    return 1 - distancia_levenshtein(a, b) / mayor


if __name__ == "__main__":
    a, b = "learning", "teaching"
    D = matriz_levenshtein(a, b)
    for fila in D:
        print(fila)
    print("Distancia:", distancia_levenshtein(a, b))
    print("Similitud:", round(similitud_levenshtein(a, b), 4))
