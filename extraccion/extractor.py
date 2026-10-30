"""
Extracción del corpus: lee los 20 PDF y guarda título, autores y abstract
de cada artículo en datos/corpus.json.

Se usa la librería PyMuPDF solo para LEER el texto de los PDF.
La búsqueda de las partes (título, autores, abstract) la hacemos nosotros.
"""
import os
import json
import pymupdf

CARPETA_PDF = os.path.join("datos", "articulos")
SALIDA = os.path.join("datos", "corpus.json")

# Palabras que marcan el inicio del abstract en los distintos formatos de revista
INICIOS_ABSTRACT = ["a b s t r a c t", "abstract:", "abstract"]

# Palabras que marcan el final del abstract
FINALES_ABSTRACT = ["keywords", "k e y w o r d s", "key words", "paper type",
                    "1. introduction", "1 introduction", "introduction"]

# Ligaduras tipográficas que trae el PDF (ﬁ, ﬂ...) y su forma normal
LIGADURAS = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl",
             "­": "", "﻿": "", "’": "'", "‘": "'", "“": '"', "”": '"'}


def limpiar(texto):
    """Cambia ligaduras y une las líneas cortadas del PDF en un solo párrafo."""
    texto = texto.replace("­\n", "")  # guion invisible al final de línea: "devel-\nopment"
    for raro, normal in LIGADURAS.items():
        texto = texto.replace(raro, normal)
    # "tech- nologies" -> "technologies" (palabra partida al final de la línea)
    texto = texto.replace("-\n", "")
    partes = texto.split()
    return " ".join(partes)


def bloques_de_texto(documento, paginas=2):
    """
    Devuelve los bloques de texto (párrafos) de las primeras páginas, en orden.
    Cada bloque es (pagina, y_arriba, y_abajo, texto).
    """
    bloques = []
    for p in range(min(paginas, len(documento))):
        for b in documento[p].get_text("blocks"):
            if b[6] == 0:  # 0 = bloque de texto (1 sería imagen)
                bloques.append((p, b[1], b[3], b[4]))
    return bloques


def empieza_con(linea, palabras):
    """True si la línea (en minúsculas y sin espacios al inicio) empieza con alguna palabra."""
    bajo = linea.strip().lower()
    for palabra in palabras:
        if bajo.startswith(palabra):
            return True
    return False


def extraer_abstract(bloques):
    """
    Recorre los bloques hasta encontrar el título "Abstract".
    Desde ahí copia línea por línea el texto del abstract, hasta que:
      - una línea empiece con un marcador de final (Keywords, Introduction...), o
      - haya un salto grande entre bloques (empieza otra sección o columna).
    El bloque de palabras clave que en algunas revistas va ANTES del texto se salta.
    """
    lineas_abstract = []
    encontrado = False
    abajo_anterior = None
    pagina_anterior = None
    for pagina, arriba, abajo, texto in bloques:
        lineas = texto.split("\n")
        if not encontrado:
            # buscar la línea que tiene la palabra "abstract"
            k = 0
            while k < len(lineas) and not empieza_con(lineas[k], INICIOS_ABSTRACT):
                k = k + 1
            if k == len(lineas):
                continue
            encontrado = True
            # quitar la palabra "abstract" de esa línea
            primera = lineas[k].strip()
            for marcador in INICIOS_ABSTRACT:
                if primera.lower().startswith(marcador):
                    primera = primera[len(marcador):].strip(" :.–-")
                    break
            lineas = [primera] + lineas[k + 1:]
        elif len(lineas_abstract) > 0:
            salto = pagina != pagina_anterior or arriba - abajo_anterior > 20
            if salto:
                break
        if len(lineas_abstract) == 0 and empieza_con(lineas[0], ["keywords", "k e y w o r d s"]):
            continue  # bloque de palabras clave antes del abstract
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


# Dos PDF no traen el autor en sus metadatos. Sus autores se tomaron
# de la primera página de cada PDF (revisado a mano).
AUTORES_SIN_METADATOS = {
    13: ["Jyoti Mudkanna Gavhane", "Reena Pagare"],
    14: ["Tamar Mikeladze", "Paulien C. Meijer", "Roald P. Verhoeff"],
}

ESPACIOS_RAROS = ["\xa0", " ", " ", " ", "\t"]


def normalizar_linea(linea):
    for raro in ESPACIOS_RAROS:
        linea = linea.replace(raro, " ")
    return linea.replace("´c", "ć").replace("∗", "*")


def separar_autores(texto):
    """
    Convierte una línea como 'Ke Zhang a,*, Ayse Begum Aslan b'
    en la lista ['Ke Zhang', 'Ayse Begum Aslan'] quitando las marcas de afiliación.
    """
    texto = texto.replace("·", ",").replace("|", ",").replace("*", "").replace(" and ", ",")
    autores = []
    for parte in texto.split(","):
        palabras = []
        for palabra in parte.split():
            # quitar números pegados al final: 'Ouyang1' -> 'Ouyang'
            while len(palabra) > 0 and palabra[-1].isdigit():
                palabra = palabra[:-1]
            # descartar marcas sueltas: 'a', 'b', '1', ''
            if len(palabra) > 1 or (len(palabra) == 1 and palabra.isupper()):
                palabras.append(palabra)
        # una persona tiene al menos nombre y apellido
        if len(palabras) >= 2:
            autores.append(" ".join(palabras))
    return autores


def extraer_autores(documento, numero):
    """
    1) Si los metadatos del PDF traen la lista completa de autores, se usa.
    2) Si solo traen el primer autor, se busca en la primera página la línea
       que tiene su apellido y se toma esa línea (y sus continuaciones).
    3) Si el PDF no tiene metadatos de autor, se usa la tabla revisada a mano.
    """
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
        # unir las líneas siguientes si la lista de autores continúa
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
    """Título de los metadatos del PDF; si no sirve, el del nombre del archivo."""
    titulo = limpiar(documento.metadata.get("title", ""))
    if titulo == "" or "_" in titulo:
        titulo = nombre[nombre.find(".") + 1: -4].strip()
    return titulo


def extraer_corpus():
    corpus = []
    archivos = os.listdir(CARPETA_PDF)
    # ordenar por el número del inicio del nombre: 1, 2, ..., 20
    archivos.sort(key=lambda nombre: int(nombre.split(".")[0]))
    for nombre in archivos:
        if not nombre.lower().endswith(".pdf"):
            continue
        documento = pymupdf.open(os.path.join(CARPETA_PDF, nombre))
        numero = int(nombre.split(".")[0])
        corpus.append({
            "id": numero,
            "archivo": nombre,
            "titulo": extraer_titulo(documento, nombre),
            "autores": extraer_autores(documento, numero),
            "abstract": extraer_abstract(bloques_de_texto(documento)),
        })
    return corpus


if __name__ == "__main__":
    datos = extraer_corpus()
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print("Artículos procesados:", len(datos))
    for art in datos:
        print(art["id"], "|", art["titulo"][:50], "|", "; ".join(art["autores"]), "|", len(art["abstract"]), "caracteres")
