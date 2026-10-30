import math


def matriz_cofenetica(fusiones, n):
    """Para cada par, la altura del dendrograma donde quedaron juntos por primera vez."""
    C = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(0.0)
        C.append(fila)
    grupos = {}
    for i in range(n):
        grupos[i] = [i]
    siguiente_id = n
    for a, b, distancia, nuevo in fusiones:
        # todos los de un lado se unen con todos los del otro a esta altura
        for x in grupos[a]:
            for y in grupos[b]:
                C[x][y] = distancia
                C[y][x] = distancia
        grupos[siguiente_id] = nuevo
        siguiente_id = siguiente_id + 1
    return C


def correlacion_pearson(xs, ys):
    n = len(xs)
    media_x = 0.0
    media_y = 0.0
    for k in range(n):
        media_x = media_x + xs[k]
        media_y = media_y + ys[k]
    media_x = media_x / n
    media_y = media_y / n
    arriba = 0.0
    suma_x2 = 0.0
    suma_y2 = 0.0
    for k in range(n):
        dx = xs[k] - media_x
        dy = ys[k] - media_y
        arriba = arriba + dx * dy
        suma_x2 = suma_x2 + dx * dx
        suma_y2 = suma_y2 + dy * dy
    if suma_x2 == 0 or suma_y2 == 0:
        return 0.0
    return arriba / math.sqrt(suma_x2 * suma_y2)


def correlacion_cofenetica(D, fusiones):
    """Qué tanto respeta el dendrograma las distancias originales (1 = perfecto)."""
    n = len(D)
    C = matriz_cofenetica(fusiones, n)
    originales = []
    cofeneticas = []
    for i in range(n):
        for j in range(i + 1, n):
            originales.append(D[i][j])
            cofeneticas.append(C[i][j])
    return correlacion_pearson(originales, cofeneticas)
