# Análisis de algoritmos en el contexto de la bibliometría

Proyecto final del curso Análisis de Algoritmos (2026-2), Universidad del Quindío.

Autor: Daniel Esteban Cifuentes Blandón

## Qué hace

Trabaja sobre los abstracts de 20 artículos científicos sobre inteligencia artificial en educación:

1. Similitud textual entre artículos (4 algoritmos clásicos y 2 basados en IA).
2. Agrupamiento jerárquico (3 criterios) con dendrogramas.
3. Búsqueda de patrones en los abstracts (KMP, Boyer-Moore y Rabin-Karp).

Los algoritmos están programados a mano, sin funciones de librerías que los resuelvan.

## Estructura

| Carpeta | Contenido |
|---|---|
| `extraccion/` | Lee los PDF y genera `datos/corpus.json` |
| `datos/` | `corpus.json` con título, autores y abstract de cada artículo |
| `preprocesamiento/` | Limpieza del texto |
| `similitud/` | Requerimiento 1 |
| `clustering/` | Requerimiento 2 |
| `busqueda/` | Requerimiento 3 |
| `salidas/` | Imágenes y tablas generadas |
| `docs/` | Documento, presentación y protocolo de uso de IA |

## Cómo ejecutar

```bash
pip install -r requirements.txt
python extraccion/extractor.py
```

Los PDF no están en el repositorio. Para volver a generar `corpus.json` hay que copiarlos en `datos/articulos/`.
