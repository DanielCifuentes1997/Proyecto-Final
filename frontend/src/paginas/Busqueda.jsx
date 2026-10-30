import { useState } from 'react'
import { LoaderCircle, Search } from 'lucide-react'
import Encabezado from '../componentes/Encabezado.jsx'
import Desplegable, { Formula, Codigo } from '../componentes/Desplegable.jsx'
import { api } from '../api.js'

const SUGERENCIAS = ['learning', 'assessment', 'higher education', 'generative artificial intelligence', 'sess']

function ms(segundos) {
  const v = segundos * 1000
  return v < 0.1 ? v.toFixed(4) + ' ms' : v.toFixed(2) + ' ms'
}

function Celdas({ texto, resaltar = [], marcar = [], indices = false, desde = 0 }) {
  return (
    <div className="flex font-mono text-xs">
      {texto.split('').map((c, k) => (
        <div key={k} className="flex w-6 shrink-0 flex-col items-center">
          {indices && <span className="h-4 text-[9px] text-tinta-suave">{desde + k}</span>}
          <span
            className={
              'flex h-6 w-6 items-center justify-center border-y border-l border-linea last:border-r ' +
              (marcar.includes(k) ? 'bg-azul text-white' : resaltar.includes(k) ? 'bg-marcador-suave' : 'bg-white')
            }
          >
            {c === ' ' ? '␣' : c}
          </span>
        </div>
      ))}
    </div>
  )
}

function FragmentoResaltado({ texto, posiciones, m }) {
  const partes = []
  let ultimo = 0
  posiciones.forEach((p, k) => {
    partes.push(<span key={'t' + k}>{texto.slice(ultimo, p)}</span>)
    partes.push(
      <mark key={'m' + k} className="marcador">
        {texto.slice(p, p + m)}
      </mark>,
    )
    ultimo = p + m
  })
  partes.push(<span key="fin">{texto.slice(ultimo)}</span>)
  return <>{partes}</>
}

function RecorridoBoyerMoore({ recorrido, patron }) {
  const { fragmento, boyer_moore } = recorrido
  const m = patron.length
  return (
    <div className="overflow-x-auto pb-2">
      <div className="inline-block">
        <Celdas texto={fragmento} indices />
        {boyer_moore.map((p, k) => {
          const encontrado = p.j < 0
          return (
            <div key={k} className="mt-1 flex items-center">
              <div style={{ width: p.s * 24 }} className="shrink-0" />
              <div className="flex font-mono text-xs">
                {patron.split('').map((c, t) => (
                  <span
                    key={t}
                    className={
                      'flex h-6 w-6 items-center justify-center border border-linea ' +
                      (encontrado ? 'bg-ia-suave text-ia' : t === p.j ? 'bg-alerta/10 text-alerta' : t > p.j ? 'bg-azul-claro' : 'bg-white text-tinta-suave')
                    }
                  >
                    {c === ' ' ? '␣' : c}
                  </span>
                ))}
              </div>
              <span className="ml-3 whitespace-nowrap text-xs text-tinta-suave">
                {encontrado ? 'coincide en ' + p.s : 'falla con "' + (p.malo === ' ' ? '␣' : p.malo) + '"'} → salta {p.salto}
              </span>
            </div>
          )
        })}
        <div style={{ width: m }} />
      </div>
    </div>
  )
}

function TablaKmp({ recorrido, patron }) {
  const filas = recorrido.kmp
  return (
    <div className="max-h-80 overflow-y-auto">
      <table className="w-full text-sm">
        <thead className="sticky top-0 bg-white">
          <tr className="border-b border-linea text-left text-tinta-suave">
            <th className="py-2 pr-4 font-medium">i (texto)</th>
            <th className="pr-4 font-medium">T[i]</th>
            <th className="pr-4 font-medium">j (patrón)</th>
            <th className="pr-4 font-medium">P[j]</th>
            <th className="font-medium">resultado</th>
          </tr>
        </thead>
        <tbody className="font-mono">
          {filas.map((f, k) => (
            <tr key={k} className="border-b border-linea/50">
              <td className="py-1 pr-4">{f.i}</td>
              <td className="pr-4">{recorrido.fragmento[f.i] === ' ' ? '␣' : recorrido.fragmento[f.i]}</td>
              <td className="pr-4">{f.j}</td>
              <td className="pr-4">{patron[f.j] === ' ' ? '␣' : patron[f.j]}</td>
              <td className={f.igual ? 'text-ia' : 'text-tinta-suave'}>{f.igual ? 'igual' : 'distinto'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function pasosHash(patron, base, primo) {
  const pasos = []
  let h = 0
  for (const c of patron) {
    const codigo = c.charCodeAt(0)
    const antes = h
    h = (h * base + codigo) % primo
    pasos.push({ c, codigo, antes, h })
  }
  return pasos
}

export default function Busqueda() {
  const [patron, setPatron] = useState('')
  const [resultado, setResultado] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState(null)

  async function buscar(texto) {
    const valor = (texto ?? patron).trim()
    if (!valor) {
      setError('Escriba un patrón para buscar.')
      return
    }
    setPatron(valor)
    setCargando(true)
    setError(null)
    try {
      setResultado(await api.buscar(valor))
    } catch (e) {
      setError(e.message)
    } finally {
      setCargando(false)
    }
  }

  const r = resultado
  const maxBusqueda = r ? Math.max(...r.algoritmos.map((a) => a.t_busqueda)) : 1

  return (
    <>
      <Encabezado titulo="Búsqueda de patrones">
        Escriba una palabra o frase y se busca su coincidencia exacta en todos los abstracts con tres algoritmos
        programados desde cero.
      </Encabezado>

      <form
        onSubmit={(e) => {
          e.preventDefault()
          buscar()
        }}
        className="mb-4 flex flex-col gap-3 sm:flex-row"
      >
        <label className="relative flex-1">
          <span className="sr-only">Patrón a buscar</span>
          <Search size={18} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-tinta-suave" aria-hidden="true" />
          <input
            value={patron}
            onChange={(e) => setPatron(e.target.value)}
            placeholder="Por ejemplo: assessment"
            className="w-full rounded-md border border-linea bg-white py-3 pl-11 pr-4 font-mono text-base focus:border-azul focus:outline-none"
          />
        </label>
        <button
          type="submit"
          disabled={cargando}
          className="inline-flex items-center justify-center gap-2 rounded-md bg-azul px-6 py-3 text-sm font-medium text-white hover:bg-tinta disabled:bg-linea"
        >
          {cargando && <LoaderCircle size={16} className="animate-spin" />}
          Buscar
        </button>
      </form>
      <div className="mb-10 flex flex-wrap items-center gap-2 text-sm text-tinta-suave">
        Pruebe con:
        {SUGERENCIAS.map((s) => (
          <button key={s} type="button" onClick={() => buscar(s)} className="rounded-md border border-linea bg-white px-2.5 py-1 font-mono text-xs text-tinta hover:border-azul">
            {s}
          </button>
        ))}
      </div>
      {error && <p className="mb-6 text-sm text-alerta">{error}</p>}

      {!r && !cargando && (
        <p className="rounded-lg border border-dashed border-linea p-8 text-center text-tinta-suave">
          Los resultados, las tablas internas de cada algoritmo y sus tiempos aparecen aquí al buscar.
        </p>
      )}

      {r && (
        <div className="space-y-10">
          <section className="rounded-lg border border-linea bg-white p-6">
            <h2 className="text-2xl">
              “{r.patron}” aparece {r.algoritmos[0].ocurrencias} {r.algoritmos[0].ocurrencias === 1 ? 'vez' : 'veces'} en{' '}
              {r.algoritmos[0].articulos} {r.algoritmos[0].articulos === 1 ? 'abstract' : 'abstracts'}
            </h2>
            <p className="mb-6 mt-1 text-sm text-tinta-suave">
              Los tres algoritmos encuentran las mismas posiciones; cambia el trabajo que hacen y el tiempo.
            </p>
            <div className="overflow-x-auto">
              <table className="w-full min-w-[640px] text-sm">
                <thead>
                  <tr className="border-b border-linea text-left text-tinta-suave">
                    <th className="py-2 pr-4 font-medium">Algoritmo</th>
                    <th className="pr-4 font-medium">Preprocesamiento</th>
                    <th className="pr-4 font-medium">Búsqueda en todos los abstracts</th>
                    <th className="pr-4 font-medium" />
                    <th className="font-medium">Colisiones</th>
                  </tr>
                </thead>
                <tbody>
                  {r.algoritmos.map((a) => (
                    <tr key={a.algoritmo} className="border-b border-linea/60">
                      <td className="py-3 pr-4 font-medium">{a.algoritmo}</td>
                      <td className="pr-4 font-mono">{ms(a.t_preprocesamiento)}</td>
                      <td className="w-1/3 pr-4">
                        <span className="block h-2.5 rounded-sm bg-papel">
                          <span className="block h-2.5 rounded-sm bg-azul" style={{ width: (100 * a.t_busqueda) / maxBusqueda + '%' }} />
                        </span>
                      </td>
                      <td className="pr-4 font-mono">{ms(a.t_busqueda)}</td>
                      <td className="font-mono">{a.algoritmo === 'Rabin-Karp' ? a.colisiones : '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="mt-3 text-xs text-tinta-suave">
              Tiempos promedio de 10 repeticiones en este servidor. El preprocesamiento depende solo del patrón; la búsqueda
              recorre todo el texto.
            </p>
          </section>

          <section>
            <h2 className="text-2xl">Tablas que se preparan antes de buscar</h2>
            <p className="mb-4 mt-1 text-sm text-tinta-suave">Calculadas para el patrón “{r.patron}” (m = {r.m}).</p>
            <div className="grid gap-4 lg:grid-cols-3">
              <div className="rounded-lg border border-linea bg-white p-5">
                <h3 className="text-lg">KMP: tabla de prefijos</h3>
                <p className="mb-3 text-xs text-tinta-suave">LPS[i]: largo del prefijo que también es sufijo hasta i.</p>
                <div className="overflow-x-auto">
                  <Celdas texto={r.patron} indices />
                  <div className="flex font-mono text-xs">
                    {r.tablas.lps.map((v, k) => (
                      <span key={k} className={'flex h-6 w-6 shrink-0 items-center justify-center border-b border-l border-linea last:border-r ' + (v > 0 ? 'bg-marcador-suave' : '')}>
                        {v}
                      </span>
                    ))}
                  </div>
                </div>
                <Codigo archivo="busqueda/kmp.py" funcion="tabla_prefijos" />
              </div>
              <div className="rounded-lg border border-linea bg-white p-5">
                <h3 className="text-lg">Boyer-Moore: carácter malo</h3>
                <p className="mb-3 text-xs text-tinta-suave">Última posición de cada carácter; si no está, −1.</p>
                <div className="flex flex-wrap gap-1 font-mono text-xs">
                  {Object.entries(r.tablas.caracter_malo).map(([c, v]) => (
                    <span key={c} className="inline-flex overflow-hidden rounded border border-linea">
                      <span className="bg-papel px-2 py-1">{c === ' ' ? '␣' : c}</span>
                      <span className="px-2 py-1">{v}</span>
                    </span>
                  ))}
                </div>
                <Codigo archivo="busqueda/boyer_moore.py" funcion="tabla_caracter_malo" />
              </div>
              <div className="rounded-lg border border-linea bg-white p-5">
                <h3 className="text-lg">Rabin-Karp: hash del patrón</h3>
                <p className="mb-3 text-xs text-tinta-suave">
                  h = (h · {r.tablas.base} + código) mod {r.tablas.primo}
                </p>
                <ol className="max-h-40 space-y-0.5 overflow-y-auto font-mono text-xs">
                  {pasosHash(r.patron, r.tablas.base, r.tablas.primo).map((p, k) => (
                    <li key={k}>
                      '{p.c === ' ' ? '␣' : p.c}' ({p.codigo}): ({p.antes}·{r.tablas.base} + {p.codigo}) mod {r.tablas.primo} = {p.h}
                    </li>
                  ))}
                </ol>
                <p className="mt-2 font-mono text-sm">
                  hash = {r.tablas.hash}, b^(m−1) mod q = {r.tablas.potencia}
                </p>
                <Codigo archivo="busqueda/rabin_karp.py" funcion="preparar_patron" />
              </div>
            </div>
          </section>

          {r.recorrido && (
            <section className="space-y-3">
              <h2 className="text-2xl">Paso a paso sobre el texto</h2>
              <p className="max-w-3xl text-sm text-tinta-suave">
                Fragmento del abstract {r.recorrido.id} alrededor de la primera coincidencia ({r.recorrido.fragmento.length}{' '}
                caracteres).
              </p>
              <Desplegable titulo="Boyer-Moore: alineaciones y saltos" resumen={r.recorrido.boyer_moore.length + ' alineaciones'} abierto>
                <p className="mb-4 max-w-3xl text-sm">
                  El patrón se compara de derecha a izquierda. En azul claro, letras que ya coincidieron; en rojo, el carácter
                  que falla; en verde, la coincidencia completa. Cada fila es una alineación y a la derecha está el salto.
                </p>
                <RecorridoBoyerMoore recorrido={r.recorrido} patron={r.patron} />
                <Formula>salto = j − última(carácter malo), mínimo 1</Formula>
                <Codigo archivo="busqueda/boyer_moore.py" funcion="buscar_boyer_moore" />
              </Desplegable>
              <Desplegable titulo="KMP: comparaciones" resumen={r.recorrido.kmp.length + ' comparaciones, el texto se lee una sola vez'}>
                <p className="mb-3 max-w-3xl text-sm">
                  i avanza por el texto y nunca retrocede. Cuando hay un fallo con j &gt; 0, j toma el valor de LPS[j − 1].
                </p>
                <TablaKmp recorrido={r.recorrido} patron={r.patron} />
                <Codigo archivo="busqueda/kmp.py" funcion="buscar_kmp" />
              </Desplegable>
              <Desplegable
                titulo="Rabin-Karp: hash de cada ventana"
                resumen={r.recorrido.rabin_karp.filter((p) => p.coincide_hash && !p.iguales).length + ' colisiones en este fragmento'}
              >
                <p className="mb-3 max-w-3xl text-sm">
                  Cada ventana de {r.m} caracteres tiene su hash, calculado desde la anterior en O(1) con rolling hash. Si el
                  hash es igual al del patrón ({r.tablas.hash}) se revisa letra por letra: verde es coincidencia real, rojo
                  es colisión.
                </p>
                <div className="flex flex-wrap gap-1 font-mono text-xs">
                  {r.recorrido.rabin_karp.map((p) => (
                    <span
                      key={p.s}
                      title={'ventana ' + p.s + ': "' + r.recorrido.fragmento.slice(p.s, p.s + r.m) + '"'}
                      className={
                        'rounded border px-1.5 py-0.5 ' +
                        (p.coincide_hash ? (p.iguales ? 'border-ia bg-ia-suave text-ia' : 'border-alerta bg-alerta/10 text-alerta') : 'border-linea bg-white text-tinta-suave')
                      }
                    >
                      {p.s}:{p.hash}
                    </span>
                  ))}
                </div>
                <Formula>h(s+1) = ((h(s) − T[s]·b^(m−1)) · b + T[s+m]) mod q</Formula>
                <Codigo archivo="busqueda/rabin_karp.py" funcion="buscar_rabin_karp" />
              </Desplegable>
              <Desplegable titulo="Complejidad" resumen="Big O del preprocesamiento y de la búsqueda">
                <table className="w-full max-w-2xl text-sm">
                  <thead>
                    <tr className="border-b border-linea text-left text-tinta-suave">
                      <th className="py-2 pr-4 font-medium">Algoritmo</th>
                      <th className="pr-4 font-medium">Preprocesamiento</th>
                      <th className="font-medium">Búsqueda</th>
                    </tr>
                  </thead>
                  <tbody className="font-mono">
                    <tr className="border-b border-linea/60"><td className="py-2 pr-4 font-sans">KMP</td><td className="pr-4">O(m)</td><td>O(n)</td></tr>
                    <tr className="border-b border-linea/60"><td className="py-2 pr-4 font-sans">Boyer-Moore</td><td className="pr-4">O(m)</td><td>mejor O(n/m), peor O(n·m)</td></tr>
                    <tr><td className="py-2 pr-4 font-sans">Rabin-Karp</td><td className="pr-4">O(m)</td><td>promedio O(n + m), peor O(n·m)</td></tr>
                  </tbody>
                </table>
                <p className="mt-3 max-w-3xl text-sm text-tinta-suave">
                  n es el largo del texto y m el del patrón. Con patrones largos Boyer-Moore salta más y es el más rápido;
                  Rabin-Karp hace aritmética modular en cada ventana y revisa las colisiones.
                </p>
              </Desplegable>
            </section>
          )}

          <section>
            <h2 className="mb-3 text-2xl">Dónde aparece</h2>
            <div className="space-y-3">
              {r.coincidencias.map((c) => (
                <details key={c.id} className="rounded-lg border border-linea bg-white">
                  <summary className="flex cursor-pointer list-none items-baseline justify-between gap-4 px-5 py-3">
                    <span className="text-sm">
                      <span className="font-mono text-xs text-tinta-suave">{c.id}</span>{' '}
                      <span className="font-medium text-tinta">{c.titulo}</span>
                    </span>
                    <span className="shrink-0 font-mono text-xs text-tinta-suave">
                      {c.posiciones.length} {c.posiciones.length === 1 ? 'vez' : 'veces'} · pos. {c.posiciones.join(', ')}
                    </span>
                  </summary>
                  <p className="border-t border-linea px-5 py-4 font-serif text-[15px] leading-7">
                    <FragmentoResaltado texto={c.texto} posiciones={c.posiciones} m={r.m} />
                  </p>
                </details>
              ))}
              {r.coincidencias.length === 0 && (
                <p className="text-sm text-tinta-suave">Ningún abstract contiene “{r.patron}”. Pruebe con otra palabra.</p>
              )}
            </div>
          </section>
        </div>
      )}
    </>
  )
}
