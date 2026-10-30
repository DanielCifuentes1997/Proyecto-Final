import os
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.servicio import Servicio

app = FastAPI(title="BiblioAnálisis API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

servicio = Servicio()


class PeticionComparar(BaseModel):
    ids: list[int]


class PeticionBuscar(BaseModel):
    patron: str


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
