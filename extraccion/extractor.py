import os
import json
import pymupdf

CARPETA_PDF = os.path.join("datos", "articulos")
SALIDA = os.path.join("datos", "corpus.json")

INICIOS_ABSTRACT = ["a b s t r a c t", "abstract:", "abstract"]
FINALES_ABSTRACT = ["keywords", "k e y w o r d s", "key words", "paper type",
                    "1. introduction", "1 introduction", "introduction"]

LIGADURAS = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl",
             "­": "", "﻿": "", "’": "'", "‘": "'", "“": '"', "”": '"'}
ESPACIOS_RAROS = ["\xa0", " ", " ", " ", "\t"]

# Estos dos PDF no traen autores en los metadatos, los saqué de la primera página
AUTORES_SIN_METADATOS = {
    13: ["Jyoti Mudkanna Gavhane", "Reena Pagare"],
    14: ["Tamar Mikeladze", "Paulien C. Meijer", "Roald P. Verhoeff"],
}


def limpiar(texto):
    """Arregla ligaduras y palabras partidas, y une todo en un solo párrafo."""
    texto = texto.replace("­\n", "")
    for raro, normal in LIGADURAS.items():
        texto = texto.replace(raro, normal)
    texto = texto.replace("-\n", "")
    return " ".join(texto.split())


def bloques_de_texto(documento, paginas=2):
    """Bloques de texto de las primeras páginas: (pagina, y_arriba, y_abajo, texto)."""
    bloques = []
    for p in range(min(paginas, len(documento))):
        for b in documento[p].get_text("blocks"):
            if b[6] == 0:
                bloques.append((p, b[1], b[3], b[4]))
    return bloques


def empieza_con(linea, palabras):
    bajo = linea.strip().lower()
    for palabra in palabras:
        if bajo.startswith(palabra):
            return True
    return False


def extraer_abstract(bloques):
    """Copia línea por línea desde 'Abstract' hasta Keywords/Introduction o un salto de sección."""
    lineas_abstract = []
    encontrado = False
    abajo_anterior = None
    pagina_anterior = None
    for pagina, arriba, abajo, texto in bloques:
        lineas = texto.split("\n")
        if not encontrado:
            # busco la línea donde empieza el abstract
            k = 0
            while k < len(lineas) and not empieza_con(lineas[k], INICIOS_ABSTRACT):
                k = k + 1
            if k == len(lineas):
                continue
            encontrado = True
            primera = lineas[k].strip()
            for marcador in INICIOS_ABSTRACT:
                if primera.lower().startswith(marcador):
                    primera = primera[len(marcador):].strip(" :.–-")
                    break
            lineas = [primera] + lineas[k + 1:]
        elif len(lineas_abstract) > 0:
            # si hay mucho espacio entre bloques ya es otra sección
            if pagina != pagina_anterior or arriba - abajo_anterior > 20:
                break
        # en Elsevier las keywords van antes del texto, las salto
        if len(lineas_abstract) == 0 and empieza_con(lineas[0], ["keywords", "k e y w o r d s"]):
            continue
        terminado = False
        for linea in lineas:
            if len(lineas_abstract) > 0 and empieza_con(linea, FINALES_ABSTRACT):
                terminado = True
                break
            if linea.strip() != "":
                lineas_abstract.append(linea)
        if terminado:
            break
        if len(lineas_abstract) > 0:
            abajo_anterior = abajo
            pagina_anterior = pagina
    return limpiar("\n".join(lineas_abstract))


def normalizar_linea(linea):
    for raro in ESPACIOS_RAROS:
        linea = linea.replace(raro, " ")
    return linea.replace("´c", "ć").replace("∗", "*")


def separar_autores(texto):
    """'Ke Zhang a,*, Ayse Begum Aslan b' -> ['Ke Zhang', 'Ayse Begum Aslan']"""
    texto = texto.replace("·", ",").replace("|", ",").replace("*", "").replace(" and ", ",")
    autores = []
    for parte in texto.split(","):
        palabras = []
        for palabra in parte.split():
            # quito los números de afiliación pegados al nombre
            while len(palabra) > 0 and palabra[-1].isdigit():
                palabra = palabra[:-1]
            if len(palabra) > 1 or (len(palabra) == 1 and palabra.isupper()):
                palabras.append(palabra)
        if len(palabras) >= 2:
            autores.append(" ".join(palabras))
    return autores


def extraer_autores(documento, numero):
    """Autores desde los metadatos o desde la línea del primer autor en la primera página."""
    meta = limpiar(normalizar_linea(documento.metadata.get("author", "")))
    if "," in meta or " and " in meta:
        return separar_autores(meta)
    if meta == "":
        return AUTORES_SIN_METADATOS.get(numero, [])
    apellido = meta.split()[-1]
    lineas = normalizar_linea(documento[0].get_text()).split("\n")
    prohibidas = ["et al", "@", "citation", "correspond"]
    for i in range(len(lineas)):
        linea = lineas[i]
        if apellido not in linea:
            continue
        valida = True
        for palabra in prohibidas:
            if palabra in linea.lower():
                valida = False
        if not valida:
            continue
        # si la lista de autores sigue en la otra línea, la uno
        texto = linea.strip()
        j = i + 1
        while j < len(lineas) and (texto.endswith(",") or texto.endswith(" and")
                                   or lineas[j].strip().startswith(",")
                                   or lineas[j].strip().startswith("and ")):
            texto = texto + " " + lineas[j].strip()
            j = j + 1
        return separar_autores(texto)
    return [meta]


def extraer_titulo(documento, nombre):
    """Título de los metadatos; si no sirve, el del nombre del archivo."""
    titulo = limpiar(documento.metadata.get("title", ""))
    if titulo == "" or "_" in titulo:
        titulo = nombre[nombre.find(".") + 1: -4].strip()
    return titulo


def extraer_articulo(ruta, numero):
    """Saca título, autores y abstract de un solo PDF."""
    nombre = os.path.basename(ruta)
    documento = pymupdf.open(ruta)
    articulo = {
        "id": numero,
        "archivo": nombre,
        "titulo": extraer_titulo(documento, nombre),
        "autores": extraer_autores(documento, numero),
        "abstract": extraer_abstract(bloques_de_texto(documento)),
    }
    documento.close()
    return articulo


def extraer_corpus():
    corpus = []
    archivos = os.listdir(CARPETA_PDF)
    archivos.sort(key=lambda nombre: int(nombre.split(".")[0]))
    for nombre in archivos:
        if not nombre.lower().endswith(".pdf"):
            continue
        numero = int(nombre.split(".")[0])
        corpus.append(extraer_articulo(os.path.join(CARPETA_PDF, nombre), numero))
    return corpus


if __name__ == "__main__":
    datos = extraer_corpus()
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print("Artículos procesados:", len(datos))
