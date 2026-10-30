import { useMemo, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FileUp, Trash2, Search, LoaderCircle } from 'lucide-react'
import Encabezado from '../componentes/Encabezado.jsx'
import MapaCalor, { colorGrupo } from '../componentes/MapaCalor.jsx'
import { useCorpus } from '../componentes/CorpusContexto.jsx'
import { api } from '../api.js'

function formatoMiles(numero) {
  return numero.toLocaleString('es-CO')
}

export default function Corpus() {
  const { corpus, mapa, error, recargar } = useCorpus()
  const [elegido, setElegido] = useState(null)
  const [filtro, setFiltro] = useState('')
  const [estado, setEstado] = useState(null)
  const [confirmar, setConfirmar] = useState(null)
  const entradaArchivo = useRef(null)
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
  const visibles = articulos.filter((a) => {
    const texto = (a.titulo + ' ' + a.autores.join(' ')).toLowerCase()
    return texto.includes(filtro.toLowerCase())
  })
  const actual = articulos.find((a) => a.id === elegido) || null
  const masLargo = articulos.reduce((m, a) => (a.palabras > m ? a.palabras : m), 0)

  async function subir(evento) {
    const archivos = Array.from(evento.target.files || [])
    evento.target.value = ''
    for (const archivo of archivos) {
      setEstado({ tipo: 'trabajando', texto: 'Extrayendo y analizando ' + archivo.name + '…' })
      try {
        const r = await api.subirPdf(archivo)
        await recargar()
        setElegido(r.id)
        setEstado({ tipo: 'ok', texto: 'Se agregó el artículo ' + r.id + ': ' + r.titulo })
      } catch (e) {
        setEstado({ tipo: 'error', texto: archivo.name + ': ' + e.message })
        return
      }
    }
  }

  async function eliminar(id) {
    setConfirmar(null)
    setEstado({ tipo: 'trabajando', texto: 'Eliminando el artículo ' + id + ' y recalculando…' })
    try {
      await api.eliminar(id)
      if (elegido === id) setElegido(null)
      await recargar()
      setEstado({ tipo: 'ok', texto: 'Se eliminó el artículo ' + id + '.' })
    } catch (e) {
      setEstado({ tipo: 'error', texto: e.message })
    }
  }

  return (
    <>
      <Encabezado
        titulo="Corpus de artículos"
        acciones={
          <>
            <input ref={entradaArchivo} type="file" accept="application/pdf" multiple className="hidden" onChange={subir} />
            <button
              type="button"
              onClick={() => entradaArchivo.current.click()}
              className="inline-flex items-center gap-2 rounded-md bg-azul px-4 py-2.5 text-sm font-medium text-white hover:bg-tinta"
            >
              <FileUp size={17} aria-hidden="true" /> Subir PDF
            </button>
          </>
        }
      >
        Abstracts, títulos y autores extraídos de los PDF. Al subir o eliminar un artículo se recalculan la similitud,
        el agrupamiento y la búsqueda.
      </Encabezado>

      {estado && (
        <div
          role="status"
          className={
            'mb-6 flex items-center gap-2 rounded-md border px-4 py-3 text-sm ' +
            (estado.tipo === 'error'
              ? 'border-alerta/40 bg-alerta/5 text-alerta'
              : estado.tipo === 'ok'
                ? 'border-ia/30 bg-ia-suave text-ia'
                : 'border-linea bg-white text-tinta-suave')
          }
        >
          {estado.tipo === 'trabajando' && <LoaderCircle className="animate-spin" size={16} />}
          {estado.texto}
        </div>
      )}

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

      <section className="mb-12 grid gap-8 xl:grid-cols-[auto_1fr]">
        <div className="rounded-lg border border-linea bg-white p-5">
          <h2 className="text-2xl">Qué tan parecidos son</h2>
          <p className="mb-4 mt-1 max-w-md text-sm text-tinta-suave">
            Similitud TF-IDF + coseno entre cada par de abstracts. Más oscuro, más vocabulario importante en común. Las
            franjas de color marcan el grupo temático de cada artículo.
          </p>
          <MapaCalor
            mapa={mapa}
            titulos={titulos}
            alElegirPar={(a, b) => navegar('/similitud?ids=' + a + ',' + b)}
          />
        </div>

        <div className="flex min-w-0 flex-col rounded-lg border border-linea bg-white">
          <div className="border-b border-linea p-4">
            <label className="relative block">
              <span className="sr-only">Filtrar artículos</span>
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-tinta-suave" aria-hidden="true" />
              <input
                value={filtro}
                onChange={(e) => setFiltro(e.target.value)}
                placeholder="Filtrar por título o autor"
                className="w-full rounded-md border border-linea bg-papel py-2 pl-9 pr-3 text-sm placeholder:text-tinta-suave/70 focus:border-azul focus:outline-none"
              />
            </label>
          </div>
          <ul className="max-h-[560px] divide-y divide-linea overflow-y-auto">
            {visibles.map((a) => (
              <li key={a.id}>
                <div
                  className={
                    'group flex items-start gap-3 px-4 py-3 ' + (elegido === a.id ? 'bg-azul-claro/60' : 'hover:bg-papel')
                  }
                >
                  <span
                    className="mt-1.5 h-2.5 w-2.5 shrink-0 rounded-full"
                    style={{ background: colorGrupo(grupoDe[a.id] ?? 0) }}
                    aria-hidden="true"
                  />
                  <button type="button" onClick={() => setElegido(a.id)} className="min-w-0 flex-1 text-left">
                    <span className="font-mono text-xs text-tinta-suave">{a.id}</span>
                    <span className="ml-2 text-sm font-medium leading-snug text-tinta">{a.titulo}</span>
                    <span className="mt-1 block truncate text-xs text-tinta-suave">{a.autores.join(', ')}</span>
                    <span className="mt-2 block h-1 rounded-full bg-papel">
                      <span
                        className="block h-1 rounded-full bg-azul/50"
                        style={{ width: (100 * a.palabras) / masLargo + '%' }}
                      />
                    </span>
                  </button>
                  {confirmar === a.id ? (
                    <span className="flex shrink-0 items-center gap-1 text-xs">
                      <button type="button" onClick={() => eliminar(a.id)} className="rounded px-2 py-1 font-medium text-alerta hover:bg-alerta/10">
                        Eliminar
                      </button>
                      <button type="button" onClick={() => setConfirmar(null)} className="rounded px-2 py-1 text-tinta-suave hover:bg-papel">
                        Cancelar
                      </button>
                    </span>
                  ) : (
                    <button
                      type="button"
                      onClick={() => setConfirmar(a.id)}
                      aria-label={'Eliminar el artículo ' + a.id}
                      className="shrink-0 rounded p-1.5 text-tinta-suave opacity-60 hover:bg-alerta/10 hover:text-alerta group-hover:opacity-100"
                    >
                      <Trash2 size={16} />
                    </button>
                  )}
                </div>
              </li>
            ))}
            {visibles.length === 0 && (
              <li className="px-4 py-6 text-sm text-tinta-suave">Ningún artículo coincide con “{filtro}”.</li>
            )}
          </ul>
          <p className="border-t border-linea px-4 py-2 text-xs text-tinta-suave">
            La barra de cada artículo indica el largo de su abstract en palabras.
          </p>
        </div>
      </section>

      <section className="rounded-lg border border-linea bg-white p-6 md:p-8">
        {actual ? (
          <article className="max-w-3xl">
            <p className="font-mono text-xs text-tinta-suave">
              Artículo {actual.id} — {actual.palabras} palabras, {actual.caracteres} caracteres
            </p>
            <h2 className="mt-2 text-3xl leading-tight">{actual.titulo}</h2>
            <p className="mt-2 text-sm text-tinta-suave">{actual.autores.join(', ')}</p>
            <p className="mt-6 font-serif text-lg leading-8 text-tinta">{actual.abstract}</p>
          </article>
        ) : (
          <p className="text-tinta-suave">Elija un artículo de la lista para leer su abstract completo.</p>
        )}
      </section>
    </>
  )
}
