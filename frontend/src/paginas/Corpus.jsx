import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, LoaderCircle, GitCompareArrows } from 'lucide-react'
import Encabezado from '../componentes/Encabezado.jsx'
import MapaCalor, { colorGrupo } from '../componentes/MapaCalor.jsx'
import { useCorpus } from '../componentes/CorpusContexto.jsx'
import { paleta } from '../componentes/paleta.js'

function formatoMiles(numero) {
  return numero.toLocaleString('es-CO')
}

function rgb(c) {
  return 'rgb(' + c.join(',') + ')'
}

export default function Corpus() {
  const { corpus, mapa, error } = useCorpus()
  const [elegido, setElegido] = useState(1)
  const [filtro, setFiltro] = useState('')
  const navegar = useNavigate()

  const grupoDe = useMemo(() => {
    const g = {}
    if (mapa) mapa.ids.forEach((id, i) => (g[id] = mapa.grupos[i]))
    return g
  }, [mapa])

  const titulos = useMemo(() => {
    const t = {}
    if (corpus) corpus.articulos.forEach((a) => (t[a.id] = a.titulo))
    return t
  }, [corpus])

  // el par más parecido según TF-IDF, para invitar a compararlo
  const masParecido = useMemo(() => {
    if (!mapa) return null
    let mejor = null
    for (let i = 0; i < mapa.ids.length; i++) {
      for (let j = i + 1; j < mapa.ids.length; j++) {
        if (!mejor || mapa.similitud[i][j] > mejor.valor) mejor = { a: mapa.ids[i], b: mapa.ids[j], valor: mapa.similitud[i][j] }
      }
    }
    return mejor
  }, [mapa])

  if (error) {
    return (
      <Encabezado titulo="Corpus de artículos">
        No se pudo conectar con el servidor: {error} Revise que el backend esté encendido.
      </Encabezado>
    )
  }
  if (!corpus || !mapa) {
    return (
      <p className="flex items-center gap-2 text-tinta-suave">
        <LoaderCircle className="animate-spin" size={18} /> Cargando el corpus…
      </p>
    )
  }

  const articulos = corpus.articulos
  const visibles = articulos.filter((a) => (a.id + ' ' + a.titulo + ' ' + a.autores.join(' ')).toLowerCase().includes(filtro.toLowerCase()))
  const actual = articulos.find((a) => a.id === elegido) || articulos[0]
  const masLargo = articulos.reduce((m, a) => (a.palabras > m ? a.palabras : m), 0)
  const cantidadGrupos = Math.max(...mapa.grupos) + 1
  const tamanos = new Array(cantidadGrupos).fill(0)
  mapa.grupos.forEach((g) => tamanos[g]++)
  let maximo = 0
  mapa.similitud.forEach((fila, i) => fila.forEach((v, j) => i !== j && v > maximo && (maximo = v)))

  return (
    <>
      <Encabezado titulo="Corpus de artículos">
        Los artículos con los que trabaja todo el proyecto. De cada PDF se extrajo el título, los autores y el abstract;
        los algoritmos trabajan sobre el abstract.
      </Encabezado>

      <dl className="mb-10 grid grid-cols-2 gap-y-4 border-b border-linea pb-6 md:grid-cols-4 md:divide-x md:divide-linea">
        {[
          [articulos.length, 'artículos'],
          [formatoMiles(corpus.total_palabras), 'palabras en los abstracts'],
          [formatoMiles(corpus.vocabulario), 'términos distintos sin stopwords'],
          [corpus.autores, 'autores'],
        ].map(([valor, etiqueta]) => (
          <div key={etiqueta} className="md:px-6 md:first:pl-0">
            <dt className="text-sm text-tinta-suave">{etiqueta}</dt>
            <dd className="font-serif text-3xl text-tinta">{valor}</dd>
          </div>
        ))}
      </dl>

      <section className="mb-14">
        <h2 className="text-2xl">Los artículos</h2>
        <p className="mb-4 mt-1 text-sm text-tinta-suave">Elija uno de la lista para leer su abstract.</p>
        <div className="grid gap-6 lg:grid-cols-[minmax(0,5fr)_minmax(0,6fr)]">
          <div className="flex min-w-0 flex-col rounded-lg border border-linea bg-white">
            <div className="border-b border-linea p-4">
              <label className="relative block">
                <span className="sr-only">Filtrar artículos</span>
                <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-tinta-suave" aria-hidden="true" />
                <input
                  value={filtro}
                  onChange={(e) => setFiltro(e.target.value)}
                  placeholder="Filtrar por número, título o autor"
                  className="w-full rounded-md border border-linea bg-papel py-2 pl-9 pr-3 text-sm focus:border-azul focus:outline-none"
                />
              </label>
            </div>
            <ul className="max-h-[600px] divide-y divide-linea overflow-y-auto">
              {visibles.map((a) => (
                <li key={a.id}>
                  <button
                    type="button"
                    onClick={() => setElegido(a.id)}
                    aria-current={actual.id === a.id}
                    className={'flex w-full items-start gap-3 px-4 py-3 text-left ' + (actual.id === a.id ? 'bg-azul-claro/70' : 'hover:bg-papel')}
                  >
                    <span className="w-5 shrink-0 pt-0.5 text-right font-mono text-xs text-tinta-suave">{a.id}</span>
                    <span className="min-w-0 flex-1">
                      <span className="block text-sm font-medium leading-snug text-tinta">{a.titulo}</span>
                      <span className="mt-1 block truncate text-xs text-tinta-suave">{a.autores.join(', ')}</span>
                    </span>
                  </button>
                </li>
              ))}
              {visibles.length === 0 && <li className="px-4 py-6 text-sm text-tinta-suave">Ningún artículo coincide con “{filtro}”.</li>}
            </ul>
          </div>

          <article className="rounded-lg border border-linea bg-white p-6 lg:sticky lg:top-6 lg:self-start">
            <p className="flex items-center gap-2 text-xs text-tinta-suave">
              <span className="h-2.5 w-2.5 rounded-full" style={{ background: colorGrupo(grupoDe[actual.id] ?? 0) }} aria-hidden="true" />
              Artículo {actual.id} · grupo temático {(grupoDe[actual.id] ?? 0) + 1}
            </p>
            <h3 className="mt-2 text-2xl leading-tight">{actual.titulo}</h3>
            <p className="mt-2 text-sm text-tinta-suave">{actual.autores.join(', ')}</p>
            <div className="mt-4 flex items-center gap-3 text-xs text-tinta-suave">
              <span className="h-1.5 w-32 rounded-full bg-papel">
                <span className="block h-1.5 rounded-full bg-azul" style={{ width: (100 * actual.palabras) / masLargo + '%' }} />
              </span>
              {actual.palabras} palabras · {actual.caracteres} caracteres
            </div>
            <p className="mt-5 max-h-[420px] overflow-y-auto pr-2 font-serif text-[17px] leading-8 text-tinta">{actual.abstract}</p>
          </article>
        </div>
      </section>

      <section>
        <h2 className="text-2xl">Qué tan parecidos son entre sí</h2>
        <p className="mb-5 mt-1 max-w-3xl text-sm text-tinta-suave">
          Cada artículo comparado con cada otro usando TF-IDF + coseno, el mismo método de la sección de similitud.
        </p>
        <div className="grid gap-6 xl:grid-cols-[auto_1fr]">
          <div className="self-start rounded-lg border border-linea bg-white p-5">
            <MapaCalor mapa={mapa} titulos={titulos} alElegirPar={(a, b) => navegar('/similitud?ids=' + a + ',' + b)} />
          </div>

          <div className="space-y-5">
            <div className="rounded-lg border border-linea bg-white p-5">
              <h3 className="text-lg">Cómo leer el mapa</h3>
              <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm leading-relaxed text-tinta">
                <li>Cada fila y cada columna es un artículo, con su número.</li>
                <li>La casilla donde se cruzan dos artículos muestra qué tan parecidos son: más oscura, más vocabulario importante en común.</li>
                <li>La diagonal es cada artículo comparado consigo mismo, por eso es la más oscura.</li>
                <li>La franja de color junto a cada número es su grupo temático, que sale del agrupamiento jerárquico.</li>
              </ol>
              <div className="mt-5">
                <p className="mb-1.5 text-xs text-tinta-suave">Escala de similitud</p>
                <span
                  className="block h-3 rounded-sm"
                  style={{ background: 'linear-gradient(to right, ' + rgb(paleta().celdaClara) + ', ' + rgb(paleta().celdaOscura) + ')' }}
                />
                <span className="mt-1 flex justify-between font-mono text-[11px] text-tinta-suave">
                  <span>0</span>
                  <span>{maximo.toFixed(2)} (el par más parecido)</span>
                </span>
              </div>
            </div>

            <div className="rounded-lg border border-linea bg-white p-5">
              <h3 className="text-lg">Grupos temáticos</h3>
              <p className="mt-1 text-sm text-tinta-suave">Average linkage cortado en {cantidadGrupos} grupos.</p>
              <ul className="mt-3 grid grid-cols-2 gap-2 text-sm">
                {tamanos.map((t, g) => (
                  <li key={g} className="flex items-center gap-2">
                    <span className="h-3 w-3 rounded-sm" style={{ background: colorGrupo(g) }} aria-hidden="true" />
                    Grupo {g + 1}: {t} {t === 1 ? 'artículo' : 'artículos'}
                  </li>
                ))}
              </ul>
            </div>

            {masParecido && (
              <div className="rounded-lg border border-linea bg-white p-5">
                <h3 className="text-lg">
                  Los más parecidos: artículo {masParecido.a} y artículo {masParecido.b}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-tinta-suave">
                  De los {(mapa.ids.length * (mapa.ids.length - 1)) / 2} pares posibles, estos dos son los que más vocabulario
                  importante comparten: su similitud TF-IDF es {masParecido.valor.toFixed(4)}. En el mapa es la casilla más
                  oscura fuera de la diagonal.
                </p>
                <dl className="mt-3 space-y-2 text-sm">
                  {[masParecido.a, masParecido.b].map((id) => (
                    <div key={id}>
                      <dt className="font-medium text-tinta">Artículo {id}</dt>
                      <dd className="text-tinta-suave">{titulos[id]}</dd>
                    </div>
                  ))}
                </dl>
                <button
                  type="button"
                  onClick={() => navegar('/similitud?ids=' + masParecido.a + ',' + masParecido.b)}
                  className="mt-4 inline-flex items-center gap-2 rounded-md bg-azul px-4 py-2 text-sm font-medium text-white hover:bg-tinta"
                >
                  <GitCompareArrows size={16} aria-hidden="true" /> Comparar el {masParecido.a} y el {masParecido.b} con los 6 algoritmos
                </button>
              </div>
            )}
          </div>
        </div>
      </section>
    </>
  )
}
