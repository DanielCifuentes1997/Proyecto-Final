import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def orden_de_hojas(fusiones, n):
    """Orden de izquierda a derecha de los documentos, recorriendo el árbol desde la raíz."""
    hijos = {}
    siguiente_id = n
    for a, b, distancia, nuevo in fusiones:
        hijos[siguiente_id] = (a, b)
        siguiente_id = siguiente_id + 1
    raiz = siguiente_id - 1
    orden = []
    pila = [raiz]
    while len(pila) > 0:
        nodo = pila.pop()
        if nodo < n:
            orden.append(nodo)
        else:
            izquierdo, derecho = hijos[nodo]
            # meto primero el derecho para sacar primero el izquierdo
            pila.append(derecho)
            pila.append(izquierdo)
    return orden


def dibujar_dendrograma(fusiones, etiquetas, titulo, ruta):
    """Dibujo el árbol con líneas: cada fusión es una 'U' invertida a la altura de su distancia."""
    n = len(etiquetas)
    orden = orden_de_hojas(fusiones, n)
    # el eje arranca un poco antes de la primera fusión para que se vean las diferencias
    base = fusiones[0][2]
    for fusion in fusiones:
        if fusion[2] < base:
            base = fusion[2]
    base = base - 0.05
    x = {}
    altura = {}
    for posicion in range(len(orden)):
        x[orden[posicion]] = posicion
        altura[orden[posicion]] = base

    fig, ax = plt.subplots(figsize=(12, 6))
    siguiente_id = n
    for a, b, distancia, nuevo in fusiones:
        ax.plot([x[a], x[a], x[b], x[b]], [altura[a], distancia, distancia, altura[b]], color="#1f3a68")
        x[siguiente_id] = (x[a] + x[b]) / 2
        altura[siguiente_id] = distancia
        siguiente_id = siguiente_id + 1

    ax.set_ylim(base, 1.0)
    ax.set_xticks(range(n))
    ax.set_xticklabels([etiquetas[i] for i in orden], rotation=90)
    ax.set_ylabel("Distancia (1 - coseno TF-IDF)")
    ax.set_title(titulo)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
