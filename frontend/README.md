# Página web del proyecto

Esta carpeta es la página web del proyecto, hecha con React, Vite y Tailwind CSS. La página no calcula nada: le pide los resultados al servidor de Python (carpeta `backend/`) y los muestra con tablas, gráficas y el paso a paso de cada algoritmo.

## Cómo ejecutarla

Primero hay que tener el servidor corriendo en el puerto 8000 (ver el README principal). Luego:

```bash
npm install
npx vite
```

La página queda en http://localhost:5173. Vite pasa al servidor todas las peticiones que empiezan por `/api` (está configurado en `vite.config.js`).

Para construir la versión que se publica:

```bash
npm run build
```

Eso genera la carpeta `dist/`, que el servidor entrega como página en la aplicación publicada.

## Secciones

| Sección | Archivo | Qué muestra | Ruta del servidor |
|---|---|---|---|
| Corpus | `src/paginas/Corpus.jsx` | Cifras del corpus, lista de artículos con su abstract, mapa de calor de similitud y grupos temáticos | `/api/corpus`, `/api/corpus/mapa` |
| Similitud textual | `src/paginas/Similitud.jsx` | Selección de dos o más artículos, resultado de los 6 algoritmos, palabras en común resaltadas y el desplegable "Cómo se calcula" de cada algoritmo | `/api/similitud` |
| Agrupamiento | `src/paginas/Clustering.jsx` | Los 3 criterios con su correlación cofenética, el dendrograma y el corte en k grupos | `/api/clustering` |
| Búsqueda de patrones | `src/paginas/Busqueda.jsx` | Apariciones del patrón, tiempos, las tablas que prepara cada algoritmo y el paso a paso sobre el texto | `/api/busqueda` |
| Acerca del proyecto | `src/paginas/Acerca.jsx` | Qué hace el proyecto, cómo está armado y cómo se usó la IA | — |

## Organización de `src/`

- `main.jsx`: arranca la aplicación y define las rutas de cada sección.
- `api.js`: las funciones que le piden datos al servidor. Si el servidor responde con un error, muestra el mensaje que él envía.
- `index.css`: la paleta de colores y los estilos generales.
- `paginas/`: una página por sección.
- `componentes/`: piezas que se repiten en varias páginas:
  - `Layout.jsx`: el menú lateral y el marco de todas las páginas.
  - `Encabezado.jsx`: el título y la descripción de cada sección.
  - `Desplegable.jsx`: los bloques que se abren y se cierran, como "Cómo se calcula".
  - `CorpusContexto.jsx`: carga el corpus una sola vez y lo comparte con todas las páginas.
  - `MapaCalor.jsx` y `Dendrograma.jsx`: los dibujos en SVG del mapa de calor y del árbol.
  - `TextoResaltado.jsx`: resalta en un abstract las palabras que se comparten.
  - `Muestra.jsx` y `paleta.js`: los colores de las leyendas y de los dibujos.

## Colores

La paleta es sobria a propósito y cada color tiene un significado fijo: el petróleo es para los algoritmos clásicos y los botones, el morado solo para los resultados de los modelos de IA, y el ámbar solo para resaltar coincidencias.

## Cómo se hizo

La página se construyó con ayuda de un asistente de inteligencia artificial (Claude), como está declarado en el protocolo de uso de IA del documento del proyecto.

El proyecto se centra en los algoritmos y su análisis, que están en las carpetas de Python (`similitud/`, `clustering/`, `busqueda/`). La página no implementa ningún algoritmo: solo pide los resultados al servidor y los muestra. Por eso se hizo de forma rápida y llegó en un solo commit ("Aplicación web del proyecto"); después se ajustó en commits más pequeños (colores, mapa de calor y la tabla de TF-IDF).
