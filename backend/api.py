import os
import sys

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.servicio import Servicio

app = FastAPI(title="BiblioAnálisis API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

servicio = Servicio()
PAGINA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")


class PeticionComparar(BaseModel):
    ids: list[int]


class PeticionBuscar(BaseModel):
    patron: str


@app.api_route("/api/salud", methods=["GET", "HEAD"])
def salud():
    """Respuesta liviana para el monitor que mantiene despierto el servidor."""
    return {"estado": "ok", "articulos": len(servicio.corpus)}


@app.get("/api/corpus")
def corpus():
    return servicio.resumen_corpus()


@app.get("/api/corpus/mapa")
def mapa():
    return servicio.mapa()


@app.post("/api/similitud")
def similitud(peticion: PeticionComparar):
    if len(peticion.ids) < 2:
        raise HTTPException(400, "Elija al menos dos artículos.")
    for id_art in peticion.ids:
        if id_art not in servicio.por_id:
            raise HTTPException(404, "No existe el artículo " + str(id_art) + ".")
    return servicio.comparar(peticion.ids)


@app.get("/api/clustering")
def clustering():
    return servicio.resultado_clustering()


@app.post("/api/busqueda")
def busqueda(peticion: PeticionBuscar):
    if peticion.patron.strip() == "":
        raise HTTPException(400, "Escriba un patrón para buscar.")
    return servicio.buscar(peticion.patron)


@app.get("/{ruta:path}")
def pagina(ruta: str):
    """Entrega la página web ya construida; las rutas de React (/similitud, /busqueda...) usan index.html."""
    archivo = os.path.normpath(os.path.join(PAGINA, ruta))
    if ruta != "" and archivo.startswith(PAGINA) and os.path.isfile(archivo):
        return FileResponse(archivo)
    indice = os.path.join(PAGINA, "index.html")
    if not os.path.isfile(indice):
        raise HTTPException(404, "La página no está construida. Ejecute npm run build en la carpeta frontend.")
    return FileResponse(indice)
