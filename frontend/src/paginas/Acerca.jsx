import { ArrowDown, ArrowRight } from 'lucide-react'
import Encabezado from '../componentes/Encabezado.jsx'

const REPOSITORIO = 'https://github.com/DanielCifuentes1997/Proyecto-Final'

const ETAPAS = [
  {
    titulo: 'Los 20 PDF',
    texto: 'Los artículos que entregó el profesor. Son el punto de partida de todo.',
    lugar: 'datos/articulos',
  },
  {
    titulo: 'Extracción',
    texto: 'Un programa abre cada PDF, encuentra el título, los autores y el abstract, y los guarda ordenados.',
    lugar: 'extraccion/extractor.py',
  },
  {
    titulo: 'Corpus',
    texto: 'Un archivo con los datos limpios de cada artículo. Desde aquí trabajan todos los algoritmos.',
    lugar: 'datos/corpus.json',
  },
  {
    titulo: 'Algoritmos',
    texto: 'Similitud, agrupamiento y búsqueda, programados a mano en Python.',
    lugar: 'similitud/, clustering/, busqueda/',
  },
  {
    titulo: 'Servidor',
    texto: 'Recibe lo que pide la página, llama al algoritmo que corresponde y devuelve el resultado.',
    lugar: 'backend/api.py',
  },
  {
    titulo: 'Esta página',
    texto: 'Muestra los resultados con tablas, gráficas y el paso a paso de cada cálculo.',
    lugar: 'frontend/',
  },
]

const CARPETAS = [
  ['extraccion/', 'Lee los PDF y saca título, autores y abstract.'],
  ['preprocesamiento/', 'Limpia el texto: minúsculas, sin signos y sin palabras vacías como "the" u "of".'],
  ['similitud/', 'Requerimiento 1: Levenshtein, Jaccard, Dice, TF-IDF con coseno y los dos modelos de IA.'],
  ['clustering/', 'Requerimiento 2: agrupamiento jerárquico, dendrogramas y correlación cofenética.'],
  ['busqueda/', 'Requerimiento 3: KMP, Boyer-Moore y Rabin-Karp, con la medición de tiempos.'],
  ['backend/', 'El servidor que conecta los algoritmos con esta página.'],
  ['frontend/', 'Esta página web.'],
  ['salidas/', 'Imágenes y tablas que generan los programas (dendrogramas, gráficas de tiempos, caso de estudio).'],
]

const HERRAMIENTAS = [
  ['Python', 'El lenguaje de todos los algoritmos.'],
  ['PyMuPDF', 'Solo para leer el texto de los PDF. La búsqueda del abstract y de los autores la hice yo.'],
  ['sentence-transformers y gensim', 'Para usar los modelos de IA ya entrenados (MiniLM y GloVe). Los vectores se calcularon una vez y quedaron guardados.'],
  ['matplotlib', 'Solo para dibujar las imágenes de los dendrogramas y de los tiempos.'],
  ['FastAPI', 'Para crear el servidor que atiende a esta página.'],
  ['React, Vite y Tailwind', 'Para construir esta página y darle el diseño.'],
  ['Git y GitHub', 'Para guardar el historial del proyecto por partes, con una rama para cada requerimiento.'],
]

function Seccion({ titulo, children }) {
  return (
    <section className="mb-12">
      <h2 className="mb-4 text-2xl">{titulo}</h2>
      {children}
    </section>
  )
}

export default function Acerca() {
  return (
    <>
      <Encabezado titulo="Acerca del proyecto">
        Proyecto final de Análisis de Algoritmos (2026-2), Universidad del Quindío. Profesor: Mg. Sergio Augusto Cardona
        Torres. Hecho por Daniel Esteban Cifuentes Blandón.
      </Encabezado>

      <Seccion titulo="De qué se trata">
        <div className="max-w-3xl space-y-4 text-base leading-relaxed text-tinta">
          <p>
            Tenemos 20 artículos científicos sobre inteligencia artificial en educación. La idea es trabajar con sus
            abstracts, el resumen que trae cada artículo al principio, y responder tres preguntas con algoritmos:
          </p>
          <ul className="space-y-2 pl-5 text-tinta">
            <li className="list-disc">
              <span className="font-medium">¿Qué tan parecidos son dos artículos?</span> Se comparan con cuatro métodos
              clásicos y dos de inteligencia artificial, y se ve en qué se diferencian sus resultados.
            </li>
            <li className="list-disc">
              <span className="font-medium">¿Qué artículos hablan de temas cercanos?</span> Se agrupan con tres criterios
              distintos y se decide cuál agrupa mejor.
            </li>
            <li className="list-disc">
              <span className="font-medium">¿Dónde aparece una palabra o frase?</span> Se busca con tres algoritmos y se
              compara cuánto trabajo hace cada uno.
            </li>
          </ul>
          <p>
            Lo importante no es solo el resultado, sino poder mostrar cómo se llega a él. Por eso cada sección tiene un
            apartado de “cómo se calcula”, con la fórmula, los números del caso y el archivo del código donde está.
          </p>
        </div>
      </Seccion>

      <Seccion titulo="Cómo está armado">
        <p className="mb-6 max-w-3xl text-tinta-suave">
          El proyecto tiene dos partes que se comunican: un servidor en Python, donde viven los algoritmos, y esta página
          web, que le pide los resultados y los muestra. El recorrido de los datos es este:
        </p>
        <ol className="flex flex-col items-stretch gap-2 lg:flex-row lg:items-stretch">
          {ETAPAS.map((e, k) => (
            <li key={e.titulo} className="flex flex-col items-center gap-2 lg:flex-1 lg:flex-row">
              <div
                className={
                  'h-full w-full rounded-lg border p-4 ' +
                  (k === 3 ? 'border-azul bg-azul text-white' : 'border-linea bg-white')
                }
              >
                <p className="font-serif text-lg leading-tight">{e.titulo}</p>
                <p className={'mt-2 text-sm leading-snug ' + (k === 3 ? 'text-white/85' : 'text-tinta-suave')}>{e.texto}</p>
                <p className={'mt-3 font-mono text-[11px] ' + (k === 3 ? 'text-white/70' : 'text-tinta-suave')}>{e.lugar}</p>
              </div>
              {k < ETAPAS.length - 1 && (
                <>
                  <ArrowDown size={18} className="shrink-0 text-tinta-suave lg:hidden" aria-hidden="true" />
                  <ArrowRight size={18} className="hidden shrink-0 text-tinta-suave lg:block" aria-hidden="true" />
                </>
              )}
            </li>
          ))}
        </ol>
        <p className="mt-6 max-w-3xl text-sm leading-relaxed text-tinta-suave">
          Separarlo así tiene una ventaja: los algoritmos no saben nada de la página. Si mañana se cambia el diseño, el
          código de los algoritmos sigue igual, y se puede probar por su cuenta desde la consola.
        </p>
      </Seccion>

      <Seccion titulo="Qué hay en cada carpeta">
        <div className="overflow-hidden rounded-lg border border-linea bg-white">
          {CARPETAS.map(([carpeta, descripcion]) => (
            <div key={carpeta} className="grid gap-1 border-b border-linea px-5 py-3 last:border-b-0 md:grid-cols-[12rem_1fr] md:gap-6">
              <span className="font-mono text-sm text-azul">{carpeta}</span>
              <span className="text-sm text-tinta">{descripcion}</span>
            </div>
          ))}
        </div>
      </Seccion>

      <Seccion titulo="Decisiones que tomé y por qué">
        <div className="grid gap-4 md:grid-cols-2">
          {[
            [
              'Los algoritmos están hechos a mano',
              'El enunciado no permite usar funciones de librerías que ya resuelvan los algoritmos. Por eso todo está con ciclos, condiciones, listas y diccionarios, para que se pueda seguir línea por línea y analizar su tiempo de ejecución.',
            ],
            [
              'Python en lugar de Java',
              'En clase trabajamos con Java, pero Python facilita mucho la parte de inteligencia artificial y la publicación de la página. El código está escrito con ciclos e índices, como en Java, para que se lea igual.',
            ],
            [
              'Los vectores de IA se calculan una sola vez',
              'Los modelos de IA pesan cientos de megas. Como los abstracts no cambian, calculé sus vectores una vez y los guardé. Así la página responde rápido y el servidor no necesita cargar los modelos.',
            ],
            [
              'Average linkage como mejor agrupamiento',
              'De los tres criterios, average tiene la correlación cofenética más alta (0,8133), es decir, su árbol es el que mejor respeta las distancias reales entre los abstracts.',
            ],
          ].map(([titulo, texto]) => (
            <div key={titulo} className="rounded-lg border border-linea bg-white p-5">
              <p className="font-medium text-tinta">{titulo}</p>
              <p className="mt-2 text-sm leading-relaxed text-tinta-suave">{texto}</p>
            </div>
          ))}
        </div>
      </Seccion>

      <Seccion titulo="Herramientas">
        <div className="overflow-hidden rounded-lg border border-linea bg-white">
          {HERRAMIENTAS.map(([nombre, uso]) => (
            <div key={nombre} className="grid gap-1 border-b border-linea px-5 py-3 last:border-b-0 md:grid-cols-[14rem_1fr] md:gap-6">
              <span className="text-sm font-medium text-tinta">{nombre}</span>
              <span className="text-sm text-tinta-suave">{uso}</span>
            </div>
          ))}
        </div>
      </Seccion>

      <Seccion titulo="Uso de inteligencia artificial">
        <div className="max-w-3xl space-y-4 rounded-lg border border-linea bg-white p-6 leading-relaxed text-tinta">
          <p>
            Usé un asistente de inteligencia artificial (Claude) como apoyo durante el proyecto: para planear el trabajo,
            proponer y revisar código, explicarme cada algoritmo paso a paso y diseñar esta página.
          </p>
          <p>
            Lo que hice yo: tomar las decisiones (qué algoritmos usar, el caso de estudio, el diseño), revisar cada parte
            antes de guardarla en el repositorio, y comprobar los resultados a mano en el cuaderno: la matriz de
            Levenshtein, los conjuntos de Jaccard y Dice, el agrupamiento con cinco artículos y las tablas de KMP,
            Boyer-Moore y Rabin-Karp.
          </p>
          <p className="text-sm text-tinta-suave">
            El detalle completo está en el protocolo de uso de IA que acompaña el documento del proyecto.
          </p>
        </div>
      </Seccion>

      <Seccion titulo="Código fuente">
        <a
          href={REPOSITORIO}
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-2 rounded-md border border-linea bg-white px-4 py-2.5 text-sm font-medium text-azul hover:border-azul"
        >
          Ver el repositorio en GitHub
        </a>
      </Seccion>
    </>
  )
}
