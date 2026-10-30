def tabla_prefijos(patron):
    """LPS[i] = largo del prefijo más largo que también es sufijo en patron[0..i]."""
    m = len(patron)
    lps = [0] * m
    largo = 0
    i = 1
    while i < m:
        if patron[i] == patron[largo]:
            largo = largo + 1
            lps[i] = largo
            i = i + 1
        else:
            if largo != 0:
                # retrocedo en el patrón usando lo que ya calculé
                largo = lps[largo - 1]
            else:
                lps[i] = 0
                i = i + 1
    return lps


def buscar_kmp(texto, patron, lps=None, pasos=None):
    """Posiciones donde aparece el patrón. Si me pasan una lista en pasos, anoto cada comparación."""
    n = len(texto)
    m = len(patron)
    if m == 0 or m > n:
        return []
    if lps is None:
        lps = tabla_prefijos(patron)
    posiciones = []
    i = 0
    j = 0
    while i < n:
        if pasos is not None:
            pasos.append((i, j, texto[i], patron[j], texto[i] == patron[j]))
        if texto[i] == patron[j]:
            i = i + 1
            j = j + 1
            if j == m:
                posiciones.append(i - m)
                j = lps[j - 1]
        else:
            if j != 0:
                # no vuelvo atrás en el texto, solo en el patrón
                j = lps[j - 1]
            else:
                i = i + 1
    return posiciones


if __name__ == "__main__":
    print(tabla_prefijos("learning"))
    print(tabla_prefijos("aabaaab"))
    print(buscar_kmp("machine learning and deep learning", "learning"))
