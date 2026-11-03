# Análisis de algoritmos en el contexto de la bibliometría

Proyecto final del curso **Análisis de Algoritmos** (2026-2), Programa de Ingeniería de Sistemas y Computación, Universidad del Quindío.

- **Autor:** Daniel Esteban Cifuentes Blandón
- **Profesor:** Mg. Sergio Augusto Cardona Torres
- **Aplicación publicada:** https://biblioanalisis.onrender.com

El proyecto trabaja con los abstracts de los 20 artículos científicos sobre inteligencia artificial en la educación que entregó el profesor. Sobre esos textos responde tres preguntas, cada una con algoritmos programados desde cero:

1. **¿Qué tan parecidos son dos o más artículos?** Similitud textual con cuatro algoritmos clásicos y dos basados en modelos de inteligencia artificial.
2. **¿Qué artículos tratan temas cercanos?** Agrupamiento jerárquico con tres criterios, sus dendrogramas y una métrica para decidir cuál agrupa mejor.
3. **¿Dónde aparece una palabra o una frase?** Búsqueda de patrones con tres algoritmos, comparando su complejidad teórica con tiempos reales.

Todo se puede usar desde la aplicación web, que muestra los resultados, las tablas internas de cada algoritmo y el archivo y la función del código donde está cada fórmula.

## Algoritmos

| Requerimiento | Algoritmo | Archivo |
|---|---|---|
| 1. Similitud | Levenshtein (programación dinámica) | `similitud/levenshtein.py` |
| | Jaccard | `similitud/jaccard.py` |
| | Dice (Sørensen–Dice) | `similitud/dice.py` |
| | TF-IDF con similitud del coseno | `similitud/tfidf_coseno.py` |
| | MiniLM y GloVe (embeddings) con coseno y distancia euclidiana | `similitud/ia_embeddings.py` |
| 2. Agrupamiento | Single, complete y average linkage | `clustering/jerarquico.py` |
| | Dendrograma | `clustering/dendrograma.py` |
| | Correlación cofenética | `clustering/metrica.py` |
| 3. Búsqueda | Knuth-Morris-Pratt | `busqueda/kmp.py` |
| | Boyer-Moore (regla del carácter malo) | `busqueda/boyer_moore.py` |
| | Rabin-Karp (hash con aritmética modular) | `busqueda/rabin_karp.py` |

Los algoritmos están escritos con ciclos, condiciones, listas y diccionarios, con índices "a lo Java", para que se puedan seguir línea por línea y contar sus instrucciones. No se usan funciones de librerías que los resuelvan: ni `find()` o `index()` para buscar, ni `sorted()`, `max()` o conjuntos de Python, ni librerías como scikit-learn o scipy. Las librerías externas solo leen los PDF, cargan los modelos preentrenados, dibujan las gráficas y arman el servidor y la página.

Para los dos modelos de IA, la librería solo entrega los vectores de cada abstract; el promedio de los vectores de GloVe, el producto punto, el coseno y la distancia euclidiana están programados en el proyecto.

## Estructura del repositorio

```
Proyecto-Final/
├── extraccion/         lectura de los PDF y estadísticas del corpus
├── preprocesamiento/   minúsculas, separación en palabras y stopwords
├── similitud/          requerimiento 1: los 6 algoritmos, el comparador y el caso de estudio
├── clustering/         requerimiento 2: distancias, agrupamiento, dendrogramas y métrica
├── busqueda/           requerimiento 3: KMP, Boyer-Moore, Rabin-Karp y medición de tiempos
├── backend/            servidor (FastAPI): rutas de la API y clase Servicio
├── frontend/           página web (React, Vite y Tailwind)
├── datos/              corpus.json (los 20 artículos) y embeddings.json (vectores de IA)
├── salidas/            gráficas y tablas que generan los programas
├── Dockerfile          construcción de la imagen que se publica en Render
└── requirements.txt    librerías de Python que usa el servidor
```

Cada carpeta de algoritmos funciona sola: no sabe nada de la página web y se puede ejecutar desde la consola. El servidor carga el corpus una vez al arrancar, deja calculados el modelo TF-IDF, la matriz de distancias y los tres agrupamientos, y la página solo muestra lo que el servidor le devuelve.

## Cómo ejecutarlo

Se necesita Python 3.11 y Node.js 22.

### 1. Servidor

```bash
python -m venv venv
venv\Scripts\activate          # en Linux o macOS: source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn backend.api:app --port 8000
```

La API queda en http://localhost:8000/api/salud.

### 2. Página web (en otra terminal)

```bash
cd frontend
npm install
npx vite
```

La página queda en http://localhost:5173 y le pide los datos al servidor del paso anterior.

### 3. Con Docker (igual que en Render)

```bash
docker build -t biblioanalisis .
docker run -p 8000:8000 biblioanalisis
```

Construye la página y el servidor en una sola imagen; todo queda en http://localhost:8000.

## Cada parte desde la consola

Con el entorno virtual activo y desde la carpeta del proyecto:

| Comando | Qué hace |
|---|---|
| `python similitud/comparar.py 11,16` | Compara los artículos indicados con los 6 algoritmos |
| `python similitud/caso_estudio.py` | Paso a paso del caso de estudio (artículos 11 y 16) |
| `python similitud/grafica_similitud.py` | Gráfica de los 6 algoritmos para el caso de estudio |
| `python similitud/todos_los_pares.py --recalcular` | Compara los 190 pares del corpus y hace sus gráficas |
| `python similitud/tiempos_similitud.py` | Mide el tiempo de los algoritmos clásicos con textos de distinto tamaño |
| `python clustering/ejecutar.py` | Agrupamiento con los 3 criterios, dendrogramas y correlación cofenética |
| `python busqueda/buscador.py assessment` | Busca un patrón en los 20 abstracts con los 3 algoritmos |
| `python busqueda/grafica_tiempos.py` | Tiempos de búsqueda según el largo del texto y del patrón |
| `python extraccion/estadisticas.py` | Cifras del corpus y palabras que aparecen en más abstracts |

Los resultados quedan en la carpeta `salidas/`.

## Datos

- `datos/corpus.json` tiene el id, el título, los autores y el abstract de cada artículo. Lo genera `extraccion/extractor.py` a partir de los PDF.
- Los PDF no están en el repositorio por derechos de autor. Para volver a generar el corpus hay que copiarlos en `datos/articulos/` y ejecutar `python extraccion/extractor.py`.
- `datos/embeddings.json` tiene los vectores de MiniLM (384 números) y GloVe (100 números) de cada abstract. Se calcularon una sola vez con `python similitud/generar_embeddings.py`, que necesita además `pip install sentence-transformers gensim` y descarga los dos modelos. Así el servidor publicado no tiene que cargar modelos de cientos de megas.

## Despliegue

La aplicación está publicada en [Render](https://render.com) como un solo servicio construido con el `Dockerfile`: primero se construye la página con Node y después se arma la imagen de Python con el servidor, los algoritmos, los datos y la página ya construida. Cada cambio en la rama `main` se vuelve a publicar automáticamente.

Como el plan gratuito apaga el servidor después de 15 minutos sin visitas, un monitor de [UptimeRobot](https://uptimerobot.com) consulta la ruta `/api/salud` cada 5 minutos para mantenerlo activo.

## Documentación

El documento del proyecto explica cada algoritmo con su fórmula, un ejemplo resuelto con datos reales, el código con sus números de línea y el análisis de su tiempo de ejecución. Incluye la arquitectura, una tabla de trazabilidad entre el documento y el código, las correcciones hechas a partir del seguimiento 1 y el protocolo de uso de herramientas de inteligencia artificial.
