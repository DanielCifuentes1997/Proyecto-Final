def tabla_caracter_malo(patron):
    """Última posición en la que aparece cada carácter del patrón."""
    ultima = {}
    for i in range(len(patron)):
        ultima[patron[i]] = i
    return ultima


def buscar_boyer_moore(texto, patron, ultima=None, pasos=None):
    """Compara de derecha a izquierda y salta con la regla del carácter malo."""
    n = len(texto)
    m = len(patron)
    if m == 0 or m > n:
        return []
    if ultima is None:
        ultima = tabla_caracter_malo(patron)
    posiciones = []
    s = 0
    while s <= n - m:
        j = m - 1
        # comparo desde el final del patrón hacia atrás
        while j >= 0 and patron[j] == texto[s + j]:
            j = j - 1
        if j < 0:
            posiciones.append(s)
            if s + m < n:
                salto = m - ultima.get(texto[s + m], -1)
            else:
                salto = 1
        else:
            # alineo el carácter malo con su última aparición en el patrón
            salto = j - ultima.get(texto[s + j], -1)
            if salto < 1:
                salto = 1
        if pasos is not None:
            malo = texto[s + j] if j >= 0 else None
            pasos.append((s, j, malo, salto))
        s = s + salto
    return posiciones


if __name__ == "__main__":
    print(tabla_caracter_malo("learning"))
    print(buscar_boyer_moore("machine learning and deep learning", "learning"))
