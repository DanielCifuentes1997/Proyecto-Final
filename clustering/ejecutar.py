import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from similitud.comparar import cargar_corpus
from clustering.distancias import matriz_distancias
from clustering.jerarquico import clustering_jerarquico, CRITERIOS
from clustering.metrica import correlacion_cofenetica
from clustering.dendrograma import dibujar_dendrograma

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(RAIZ, "salidas", "req2")

NOMBRES = {"single": "Single linkage", "complete": "Complete linkage", "average": "Average linkage"}


def ejecutar_clustering():
    corpus, por_id = cargar_corpus()
    abstracts = []
    etiquetas = []
    for art in corpus:
        abstracts.append(art["abstract"])
        etiquetas.append("Art. " + str(art["id"]))
    D = matriz_distancias(abstracts)
    os.makedirs(CARPETA, exist_ok=True)
    resultados = []
    for criterio in CRITERIOS:
        inicio = time.perf_counter()
        fusiones = clustering_jerarquico(D, criterio)
        segundos = time.perf_counter() - inicio
        cofenetica = correlacion_cofenetica(D, fusiones)
        ruta = os.path.join(CARPETA, "dendrograma_" + criterio + ".png")
        dibujar_dendrograma(fusiones, etiquetas, NOMBRES[criterio] + " (correlación cofenética = %.4f)" % cofenetica, ruta)
        resultados.append({"criterio": criterio, "cofenetica": cofenetica, "segundos": segundos,
                           "fusiones": fusiones, "imagen": ruta})
    # guardo la métrica de los tres para comparar
    with open(os.path.join(CARPETA, "metricas.csv"), "w", encoding="utf-8") as f:
        f.write("criterio,correlacion_cofenetica,segundos\n")
        for r in resultados:
            f.write("%s,%.4f,%.4f\n" % (r["criterio"], r["cofenetica"], r["segundos"]))
    return D, etiquetas, resultados


if __name__ == "__main__":
    D, etiquetas, resultados = ejecutar_clustering()
    for r in resultados:
        print("%-9s cofenética = %.4f   (%.3f s)" % (r["criterio"], r["cofenetica"], r["segundos"]))
    mejor = resultados[0]
    for r in resultados:
        if r["cofenetica"] > mejor["cofenetica"]:
            mejor = r
    print("Más coherente:", mejor["criterio"])
