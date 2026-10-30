import { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { LoaderCircle, Search, X } from 'lucide-react'
import Encabezado from '../componentes/Encabezado.jsx'
import Desplegable, { Formula, Codigo } from '../componentes/Desplegable.jsx'
import TextoResaltado from '../componentes/TextoResaltado.jsx'
import Muestra from '../componentes/Muestra.jsx'
import { useCorpus } from '../componentes/CorpusContexto.jsx'
import { api } from '../api.js'

function f4(x) {
  return x === null || x === undefined ? '—' : x.toFixed(4)
}

function tiempo(segundos) {
  if (segundos >= 0.1) return segundos.toFixed(2) + ' s'
  return (segundos * 1000).toFixed(segundos * 1000 < 0.1 ? 4 : 2) + ' ms'
}

function Selector({ articulos, seleccion, setSeleccion }) {
  const [filtro, setFiltro] = useState('')
  const visibles = articulos.filter((a) => (a.id + ' ' + a.titulo).toLowerCase().includes(filtro.toLowerCase()))
  function alternar(id) {
    setSeleccion(seleccion.includes(id) ? seleccion.filter((x) => x !== id) : [...seleccion, id])
  }
  return (
    <div className="rounded-lg border border-linea bg-white">
      <div className="border-b border-linea p-4">
        <label className="relative block">
          <span className="sr-only">Buscar artículo</span>
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-tinta-suave" aria-hidden="true" />
          <input
            value={filtro}
            onChange={(e) => setFiltro(e.target.value)}
            placeholder="Buscar por número o título"
            className="w-full rounded-md border border-linea bg-papel py-2 pl-9 pr-3 text-sm focus:border-azul focus:outline-none"
          />
        </label>
      </div>
      <ul className="max-h-72 overflow-y-auto py-1">
        {visibles.map((a) => (
          <li key={a.id}>
            <label className="flex cursor-pointer items-start gap-3 px-4 py-2 text-sm hover:bg-papel">
              <input
                type="checkbox"
                checked={seleccion.includes(a.id)}
                onChange={() => alternar(a.id)}
                className="mt-0.5 h-4 w-4 accent-azul"
              />
              <span>
                <span className="font-mono text-xs text-tinta-suave">{a.id}</span>{' '}
                <span className="text-tinta">{a.titulo}</span>
              </span>
            </label>
          </li>
        ))}
      </ul>
    </div>
  )
}

function Barras({ resultados }) {
  return (
    <div className="space-y-3">
      {resultados.map((r) => (
        <div key={r.algoritmo} className="grid grid-cols-[9rem_1fr_4.5rem] items-center gap-3 text-sm md:grid-cols-[11rem_1fr_5rem_5.5rem]">
          <span className={r.tipo === 'ia' ? 'font-medium text-ia' : 'font-medium text-tinta'}>{r.algoritmo}</span>
          <span className="h-3 rounded-sm bg-papel">
            {r.valor !== null && (
              <span
                className={'block h-3 rounded-sm ' + (r.tipo === 'ia' ? 'bg-ia' : 'bg-azul')}
                style={{ width: Math.max(r.valor * 100, 0.5) + '%' }}
              />
            )}
          </span>
          <span className="text-right font-mono text-tinta">{r.valor === null ? 'sin vector' : f4(r.valor)}</span>
          <span className="hidden text-right font-mono text-xs text-tinta-suave md:block">{tiempo(r.segundos)}</span>
        </div>
      ))}
      <p className="pt-1 text-xs text-tinta-suave">
        <Muestra clase="bg-azul" />algoritmos clásicos <Muestra clase="bg-ia" />modelos de IA. La última columna es el tiempo de cálculo.
      </p>
    </div>
  )
}

function MatrizLevenshtein({ datos }) {
  const { a, b, matriz } = datos
  const n = a.length
  const m = b.length
  const ver = (c) => (c === ' ' ? '␣' : c)
  return (
    <div className="overflow-x-auto">
      <table className="border-collapse font-mono text-xs">
        <thead>
          <tr>
            <th className="h-7 w-7" />
            <th className="h-7 w-7 text-tinta-suave">ε</th>
            {b.split('').map((c, j) => (
              <th key={j} className="h-7 w-7 font-medium text-azul">
                {ver(c)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {matriz.map((fila, i) => (
            <tr key={i}>
              <th className="h-7 w-7 font-medium text-azul">{i === 0 ? 'ε' : ver(a[i - 1])}</th>
              {fila.map((v, j) => {
                const final = i === n && j === m
                const iguales = i > 0 && j > 0 && a[i - 1] === b[j - 1]
                return (
                  <td
                    key={j}
                    className={
                      'h-7 w-7 border border-linea text-center ' +
                      (final ? 'bg-azul font-medium text-white' : iguales ? 'bg-marcador-suave' : i === 0 || j === 0 ? 'bg-papel text-tinta-suave' : 'bg-white')
                    }
                  >
                    {v}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function DetallePar({ par, articulos }) {
  const { detalle } = par
  const A = articulos.find((x) => x.id === par.a)
  const B = articulos.find((x) => x.id === par.b)
  const comunes = useMemo(() => new Set(detalle.comunes), [detalle])
  const valor = (nombre) => par.resultados.find((r) => r.algoritmo === nombre)
  const union = detalle.tam_a + detalle.tam_b - detalle.comunes.length
  const lev = valor('Levenshtein')
  const cos = valor('TF-IDF + coseno')
  const angulo = cos && cos.valor !== null ? (Math.acos(Math.min(cos.valor, 1)) * 180) / Math.PI : null

  return (
    <div className="space-y-8">
      <section className="rounded-lg border border-linea bg-white p-6">
        <h2 className="text-2xl">
          Artículo {par.a} y artículo {par.b}
        </h2>
        <p className="mb-6 mt-1 text-sm text-tinta-suave">Similitud entre 0 (nada en común) y 1 (iguales).</p>
        <Barras resultados={par.resultados} />
      </section>

      <section>
        <h2 className="text-2xl">Vocabulario en común</h2>
        <p className="mb-4 mt-1 text-sm text-tinta-suave">
          Resaltadas las {detalle.comunes.length} palabras (sin stopwords) que aparecen en los dos abstracts. Son las que
          usan Jaccard, Dice y TF-IDF.
        </p>
        <div className="grid gap-4 lg:grid-cols-2">
          {[A, B].map((art) => (
            <article key={art.id} className="rounded-lg border border-linea bg-white p-5">
              <p className="font-mono text-xs text-tinta-suave">Artículo {art.id}</p>
              <h3 className="mt-1 text-lg leading-snug">{art.titulo}</h3>
              <p className="mt-3 font-serif text-[15px] leading-7 text-tinta">
                <TextoResaltado texto={art.abstract} palabras={comunes} />
              </p>
            </article>
          ))}
        </div>
      </section>

      <section className="space-y-3">
        <h2 className="text-2xl">Cómo se calcula cada uno</h2>

        <Desplegable titulo="Levenshtein" resumen={'Distancia de edición con programación dinámica — similitud ' + f4(lev.valor)}>
          <p className="max-w-3xl text-sm leading-relaxed">
            Cuenta el mínimo de operaciones (insertar, borrar o cambiar una letra) para convertir un texto en el otro. Se
            llena una matriz: cada casilla toma el menor valor entre la de arriba + 1, la de la izquierda + 1 y la diagonal
            + costo (0 si las letras son iguales, 1 si no).
          </p>
          <Formula>D[i][j] = mín( D[i-1][j] + 1, D[i][j-1] + 1, D[i-1][j-1] + costo ) · similitud = 1 − D[n][m] / máx(n, m)</Formula>
          <p className="mb-3 text-sm text-tinta-suave">
            Matriz con los primeros {detalle.levenshtein.a.length} caracteres de cada abstract (en ámbar, letras iguales). La
            matriz completa tiene {detalle.levenshtein.casillas_completas.toLocaleString('es-CO')} casillas.
          </p>
          <MatrizLevenshtein datos={detalle.levenshtein} />
          <Codigo archivo="similitud/levenshtein.py" funcion="matriz_levenshtein" />
        </Desplegable>

        <Desplegable titulo="Jaccard y Dice" resumen="Comparan los conjuntos de palabras de cada abstract">
          <div className="grid gap-6 md:grid-cols-2">
            <div>
              <Formula>J = |A ∩ B| / |A ∪ B|</Formula>
              <p className="font-mono text-sm">
                |A| = {detalle.tam_a}, |B| = {detalle.tam_b}, |A ∩ B| = {detalle.comunes.length}
                <br />
                |A ∪ B| = {detalle.tam_a} + {detalle.tam_b} − {detalle.comunes.length} = {union}
                <br />J = {detalle.comunes.length} / {union} = {f4(valor('Jaccard').valor)}
              </p>
              <Codigo archivo="similitud/jaccard.py" funcion="similitud_jaccard" />
            </div>
            <div>
              <Formula>D = 2 · |A ∩ B| / (|A| + |B|)</Formula>
              <p className="font-mono text-sm">
                D = 2 · {detalle.comunes.length} / ({detalle.tam_a} + {detalle.tam_b})
                <br />D = {2 * detalle.comunes.length} / {detalle.tam_a + detalle.tam_b} = {f4(valor('Dice').valor)}
              </p>
              <Codigo archivo="similitud/dice.py" funcion="similitud_dice" />
            </div>
          </div>
        </Desplegable>

        <Desplegable titulo="TF-IDF + coseno" resumen={'Pesos de las palabras y ángulo entre los vectores — ' + f4(cos.valor)}>
          <p className="max-w-3xl text-sm leading-relaxed">
            Cada palabra pesa más si se repite en el abstract (tf) y si casi ningún otro abstract la usa (idf). Solo las
            palabras comunes aportan al producto punto.
          </p>
          <Formula>idf = log10(N / df) · peso = tf · idf · cos θ = A·B / (|A| · |B|)</Formula>
          <div className="overflow-x-auto">
            <table className="w-full min-w-[640px] text-sm">
              <thead>
                <tr className="border-b border-linea text-left text-tinta-suave">
                  {['Palabra', 'tf A', 'tf B', 'df', 'idf', 'peso A', 'peso B', 'A × B'].map((t) => (
                    <th key={t} className="py-2 pr-4 font-medium">
                      {t}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="font-mono">
                {detalle.tfidf.map((f) => (
                  <tr key={f.palabra} className="border-b border-linea/60">
                    <td className="py-1.5 pr-4 font-sans">{f.palabra}</td>
                    <td className="pr-4">{f.tf_a}</td>
                    <td className="pr-4">{f.tf_b}</td>
                    <td className="pr-4">{f.df}</td>
                    <td className="pr-4">{f4(f.idf)}</td>
                    <td className="pr-4">{f4(f.peso_a)}</td>
                    <td className="pr-4">{f4(f.peso_b)}</td>
                    <td className={'pr-4 ' + (f.producto > 0 ? 'text-azul' : 'text-tinta-suave')}>{f4(f.producto)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-4 font-mono text-sm leading-7">
            N = {detalle.n_documentos} abstracts
            <br />
            A·B = {f4(detalle.producto_punto)} &nbsp; |A| = {f4(detalle.magnitud_a)} &nbsp; |B| = {f4(detalle.magnitud_b)}
            <br />
            cos θ = {f4(detalle.producto_punto)} / ({f4(detalle.magnitud_a)} · {f4(detalle.magnitud_b)}) = {f4(cos.valor)}
            {angulo !== null && <> &nbsp; → θ = {angulo.toFixed(2)}°</>}
          </p>
          <Codigo archivo="similitud/tfidf_coseno.py" funcion="vector_tfidf, coseno" />
        </Desplegable>

        <Desplegable titulo="Modelos de IA: MiniLM y GloVe" resumen="Embeddings preentrenados comparados con coseno">
          <p className="max-w-3xl text-sm leading-relaxed">
            MiniLM (all-MiniLM-L6-v2) lee el abstract completo y lo convierte en un vector de 384 números. GloVe tiene un
            vector de 100 números por palabra; el vector del abstract es el promedio de sus palabras. Los dos vectores se
            comparan con el coseno, programado a mano igual que en TF-IDF.
          </p>
          <Formula>cos θ = Σ aₖ·bₖ / ( √Σ aₖ² · √Σ bₖ² ) · euclidiana = √Σ (aₖ − bₖ)²</Formula>
          <div className="grid gap-3 font-mono text-sm md:grid-cols-2">
            {['MiniLM', 'GloVe'].map((nombre) => {
              const r = valor(nombre)
              return (
                <p key={nombre}>
                  {nombre}: coseno {r.valor === null ? 'sin vector' : f4(r.valor)}
                  {r.euclidiana !== undefined && <>, distancia euclidiana {f4(r.euclidiana)}</>}
                </p>
              )
            })}
          </div>
          <Codigo archivo="similitud/ia_embeddings.py" funcion="similitud_coseno, distancia_euclidiana" />
        </Desplegable>
      </section>
    </div>
  )
}

export default function Similitud() {
  const { corpus } = useCorpus()
  const [parametros] = useSearchParams()
  const [seleccion, setSeleccion] = useState([])
  const [resultado, setResultado] = useState(null)
  const [parActivo, setParActivo] = useState(0)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState(null)

  async function comparar(ids) {
    setCargando(true)
    setError(null)
    try {
      const r = await api.comparar(ids)
      setResultado(r)
      setParActivo(0)
    } catch (e) {
      setError(e.message)
    } finally {
      setCargando(false)
    }
  }

  useEffect(() => {
    const ids = (parametros.get('ids') || '')
      .split(',')
      .map(Number)
      .filter((x) => x > 0)
    if (ids.length >= 2) {
      setSeleccion(ids)
      comparar(ids)
    }
  }, [parametros])

  if (!corpus) return null
  const articulos = corpus.articulos
  const pares = resultado ? resultado.pares : []

  return (
    <>
      <Encabezado titulo="Similitud textual">
        Elija dos o más artículos. Cada par se compara con 4 algoritmos clásicos y 2 modelos de inteligencia artificial.
      </Encabezado>

      <section className="mb-10 grid gap-6 lg:grid-cols-[1fr_18rem]">
        <Selector articulos={articulos} seleccion={seleccion} setSeleccion={setSeleccion} />
        <div className="flex flex-col gap-3">
          <p className="text-sm text-tinta-suave">
            {seleccion.length < 2
              ? 'Marque al menos dos artículos.'
              : seleccion.length + ' artículos: ' + ((seleccion.length * (seleccion.length - 1)) / 2 === 1 ? 'se comparará 1 par.' : 'se compararán ' + (seleccion.length * (seleccion.length - 1)) / 2 + ' pares.')}
          </p>
          <div className="flex flex-wrap gap-2">
            {seleccion.map((id) => (
              <span key={id} className="inline-flex items-center gap-1 rounded-md border border-linea bg-white px-2 py-1 font-mono text-xs">
                {id}
                <button
                  type="button"
                  aria-label={'Quitar el artículo ' + id}
                  onClick={() => setSeleccion(seleccion.filter((x) => x !== id))}
                  className="text-tinta-suave hover:text-tinta"
                >
                  <X size={13} />
                </button>
              </span>
            ))}
          </div>
          <button
            type="button"
            disabled={seleccion.length < 2 || cargando}
            onClick={() => comparar(seleccion)}
            className="mt-auto inline-flex items-center justify-center gap-2 rounded-md bg-azul px-4 py-2.5 text-sm font-medium text-white hover:bg-tinta disabled:cursor-not-allowed disabled:bg-linea disabled:text-tinta-suave"
          >
            {cargando && <LoaderCircle size={16} className="animate-spin" />}
            {cargando ? 'Comparando…' : 'Comparar'}
          </button>
          {error && <p className="text-sm text-alerta">{error}</p>}
        </div>
      </section>

      {pares.length > 1 && (
        <section className="mb-8">
          <h2 className="mb-3 text-2xl">Todos los pares</h2>
          <div className="overflow-x-auto rounded-lg border border-linea bg-white">
            <table className="w-full min-w-[720px] text-sm">
              <thead>
                <tr className="border-b border-linea text-left text-tinta-suave">
                  <th className="px-4 py-2 font-medium">Par</th>
                  {pares[0].resultados.map((r) => (
                    <th key={r.algoritmo} className={'px-3 py-2 font-medium ' + (r.tipo === 'ia' ? 'text-ia' : '')}>
                      {r.algoritmo}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="font-mono">
                {pares.map((p, k) => (
                  <tr
                    key={p.a + '-' + p.b}
                    onClick={() => setParActivo(k)}
                    className={'cursor-pointer border-b border-linea/60 ' + (k === parActivo ? 'bg-azul-claro/60' : 'hover:bg-papel')}
                  >
                    <td className="px-4 py-2 font-sans">
                      {p.a} y {p.b}
                    </td>
                    {p.resultados.map((r) => (
                      <td key={r.algoritmo} className="px-3 py-2">
                        {f4(r.valor)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-2 text-xs text-tinta-suave">Haga clic en un par para ver su detalle.</p>
        </section>
      )}

      {pares.length > 0 && <DetallePar par={pares[parActivo]} articulos={articulos} />}
    </>
  )
}
