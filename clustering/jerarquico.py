CRITERIOS = ["single", "complete", "average"]


def distancia_entre_grupos(D, grupo_a, grupo_b, criterio):
    """single = la menor, complete = la mayor, average = el promedio de las distancias entre sus elementos."""
    menor = None
    mayor = None
    suma = 0.0
    for i in range(len(grupo_a)):
        for j in range(len(grupo_b)):
            d = D[grupo_a[i]][grupo_b[j]]
            if menor is None or d < menor:
                menor = d
            if mayor is None or d > mayor:
                mayor = d
            suma = suma + d
    if criterio == "single":
        return menor
    if criterio == "complete":
        return mayor
    return suma / (len(grupo_a) * len(grupo_b))


def clustering_jerarquico(D, criterio):
    """
    Empieza con cada documento en su propio grupo y en cada paso une los dos grupos más cercanos.
    Devuelve la lista de fusiones: (id_grupo_a, id_grupo_b, distancia, elementos del nuevo grupo).
    Los documentos son los grupos 0..n-1 y cada fusión crea el grupo n, n+1, ...
    """
    n = len(D)
    activos = {}
    for i in range(n):
        activos[i] = [i]
    fusiones = []
    siguiente_id = n
    while len(activos) > 1:
        ids = list(activos.keys())
        mejor_a = None
        mejor_b = None
        mejor_d = None
        # busco el par de grupos más cercano
        for x in range(len(ids)):
            for y in range(x + 1, len(ids)):
                d = distancia_entre_grupos(D, activos[ids[x]], activos[ids[y]], criterio)
                if mejor_d is None or d < mejor_d:
                    mejor_a = ids[x]
                    mejor_b = ids[y]
                    mejor_d = d
        nuevo = activos[mejor_a] + activos[mejor_b]
        fusiones.append((mejor_a, mejor_b, mejor_d, nuevo))
        del activos[mejor_a]
        del activos[mejor_b]
        activos[siguiente_id] = nuevo
        siguiente_id = siguiente_id + 1
    return fusiones


def cortar_en_grupos(fusiones, n, k):
    """Aplico solo las primeras n-k fusiones y quedan k grupos. Devuelve el grupo de cada documento."""
    grupos = {}
    for i in range(n):
        grupos[i] = [i]
    siguiente_id = n
    for paso in range(n - k):
        a, b, distancia, nuevo = fusiones[paso]
        del grupos[a]
        del grupos[b]
        grupos[siguiente_id] = nuevo
        siguiente_id = siguiente_id + 1
    etiqueta = [0] * n
    numero = 0
    for clave in grupos:
        for doc in grupos[clave]:
            etiqueta[doc] = numero
        numero = numero + 1
    return etiqueta
