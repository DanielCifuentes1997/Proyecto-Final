BASE = 256
PRIMO = 101


def hash_inicial(cadena, m, base=BASE, primo=PRIMO):
    """h = (c0·b^(m-1) + c1·b^(m-2) + ... + c(m-1)) mod q, calculado con Horner."""
    h = 0
    for i in range(m):
        h = (h * base + ord(cadena[i])) % primo
    return h


def preparar_patron(patron, base=BASE, primo=PRIMO):
    """Hash del patrón y b^(m-1) mod q (sirve para quitar el carácter que sale de la ventana)."""
    m = len(patron)
    potencia = 1
    for i in range(m - 1):
        potencia = (potencia * base) % primo
    return hash_inicial(patron, m, base, primo), potencia


def buscar_rabin_karp(texto, patron, preparado=None, base=BASE, primo=PRIMO, pasos=None):
    """Compara hashes; si coinciden, reviso letra por letra para descartar colisiones."""
    n = len(texto)
    m = len(patron)
    if m == 0 or m > n:
        return [], 0
    if preparado is None:
        preparado = preparar_patron(patron, base, primo)
    hp, potencia = preparado
    ht = hash_inicial(texto, m, base, primo)
    posiciones = []
    colisiones = 0
    for s in range(n - m + 1):
        iguales = None
        if hp == ht:
            iguales = True
            k = 0
            while k < m and iguales:
                if texto[s + k] != patron[k]:
                    iguales = False
                k = k + 1
            if iguales:
                posiciones.append(s)
            else:
                colisiones = colisiones + 1
        if pasos is not None:
            pasos.append((s, ht, hp == ht, iguales))
        # rolling hash: saco el carácter de la izquierda y meto el siguiente
        if s < n - m:
            ht = ((ht - ord(texto[s]) * potencia) * base + ord(texto[s + m])) % primo
    return posiciones, colisiones


if __name__ == "__main__":
    print(hash_inicial("learning", 8))
    print(buscar_rabin_karp("machine learning and deep learning", "learning"))
