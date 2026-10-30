import { useEffect, useMemo, useState } from 'react'
import { LoaderCircle } from 'lucide-react'
import Encabezado from '../componentes/Encabezado.jsx'
import Dendrograma, { gruposAlCortar, colorDeGrupo } from '../componentes/Dendrograma.jsx'
import Desplegable, { Formula, Codigo } from '../componentes/Desplegable.jsx'
import { useCorpus } from '../componentes/CorpusContexto.jsx'
import { api } from '../api.js'

const NOMBRES = {
  single: { titulo: 'Single linkage', regla: 'la menor distancia entre sus artículos' },
  complete: { titulo: 'Complete linkage', regla: 'la mayor distancia entre sus artículos' },
  average: { titulo: 'Average linkage', regla: 'el promedio de todas las distancias entre sus artículos' },
}

export default function Clustering() {
  const { version } = useCorpus()
  const [datos, setDatos] = useState(null)
  const [error, setError] = useState(null)
  const [activo, setActivo] = useState('average')
  const [k, setK] = useState(4)

  useEffect(() => {
    api
      .clustering()
      .then((d) => {
        setDatos(d)
        setError(null)
      })
      .catch((e) => setError(e.message))
  }, [version])

  const mejor = useMemo(() => {
    if (!datos) return null
    return datos.criterios.reduce((m, c) => (c.cofenetica > m.cofenetica ? c : m), datos.criterios[0])
  }, [datos])

  if (error) return <Encabezado titulo="Agrupamiento jerárquico">No se pudo cargar: {error}</Encabezado>
  if (!datos) {
    return (
      <p className="flex items-center gap-2 text-tinta-suave">
        <LoaderCircle className="animate-spin" size={18} /> Calculando los agrupamientos…
      </p>
    )
  }

  const n = datos.etiquetas.length
  const kSeguro = Math.min(Math.max(k, 2), Math.max(n - 1, 2))
  const criterio = datos.criterios.find((c) => c.criterio === activo)
  const { grupoDe } = gruposAlCortar(criterio.fusiones, n, kSeguro)
  const grupos = []
  for (let g = 0; g < kSeguro; g++) grupos.push([])
  grupoDe.forEach((g, doc) => grupos[g] && grupos[g].push(datos.etiquetas[doc]))

  return (
    <>
      <Encabezado titulo="Agrupamiento jerárquico">
        Los {n} abstracts se agrupan de abajo hacia arriba: en cada paso se unen los dos grupos más parecidos. Los tres
        criterios cambian cómo se mide la distancia entre grupos.
      </Encabezado>

      <section className="mb-8 grid gap-4 md:grid-cols-3" aria-label="Comparación de criterios">
        {datos.criterios.map((c) => {
          const elegido = c.criterio === activo
          const esMejor = mejor && c.criterio === mejor.criterio
          return (
            <button
              key={c.criterio}
              type="button"
              onClick={() => setActivo(c.criterio)}
              aria-pressed={elegido}
              className={
                'rounded-lg border bg-white p-5 text-left transition-colors ' +
                (elegido ? 'border-azul ring-1 ring-azul' : 'border-linea hover:border-tinta-suave')
              }
            >
              <span className="flex items-baseline justify-between gap-2">
                <span className="font-serif text-xl text-tinta">{NOMBRES[c.criterio].titulo}</span>
                {esMejor && <span className="rounded bg-marcador-suave px-2 py-0.5 text-xs text-[#7a5c0c]">más coherente</span>}
              </span>
              <span className="mt-1 block text-sm text-tinta-suave">Distancia entre grupos: {NOMBRES[c.criterio].regla}.</span>
              <span className="mt-4 block text-xs text-tinta-suave">Correlación cofenética</span>
              <span className="mt-1 flex items-center gap-3">
                <span className="h-2 flex-1 rounded-sm bg-papel">
                  <span className="block h-2 rounded-sm bg-azul" style={{ width: c.cofenetica * 100 + '%' }} />
                </span>
                <span className="font-mono text-sm text-tinta">{c.cofenetica.toFixed(4)}</span>
              </span>
            </button>
          )
        })}
      </section>

      <section className="mb-8 rounded-lg border border-linea bg-white p-6">
        <div className="mb-4 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <h2 className="text-2xl">Dendrograma: {NOMBRES[activo].titulo}</h2>
            <p className="mt-1 text-sm text-tinta-suave">
              La altura de cada unión es la distancia (1 − coseno TF-IDF) a la que se juntaron los grupos.
            </p>
          </div>
          <label className="flex items-center gap-3 text-sm text-tinta-suave">
            Cortar en
            <input
              type="range"
              min={2}
              max={Math.min(8, n - 1)}
              value={kSeguro}
              onChange={(e) => setK(Number(e.target.value))}
              className="w-32 accent-azul"
            />
            <span className="w-16 font-mono text-tinta">{kSeguro} grupos</span>
          </label>
        </div>
        <Dendrograma criterio={criterio} etiquetas={datos.etiquetas} k={kSeguro} />
      </section>

      <section className="mb-10">
        <h2 className="mb-3 text-2xl">Grupos al cortar el árbol</h2>
        <div className="grid gap-4 md:grid-cols-2">
          {grupos.map((lista, g) => (
            <div key={g} className="rounded-lg border border-linea bg-white p-5">
              <p className="mb-3 flex items-center gap-2 text-sm font-medium text-tinta">
                <span className="h-3 w-3 rounded-full" style={{ background: colorDeGrupo(g) }} aria-hidden="true" />
                Grupo {g + 1} — {lista.length} {lista.length === 1 ? 'artículo' : 'artículos'}
              </p>
              <ul className="space-y-1.5 text-sm">
                {lista.map((e) => (
                  <li key={e.id} className="flex gap-2">
                    <span className="w-6 shrink-0 text-right font-mono text-xs leading-5 text-tinta-suave">{e.id}</span>
                    <span className="text-tinta">{e.titulo}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      <section className="space-y-3">
        <h2 className="text-2xl">Cómo se calcula</h2>
        <Desplegable titulo="Distancia entre abstracts" resumen="1 − coseno de los vectores TF-IDF">
          <p className="max-w-3xl text-sm leading-relaxed">
            Cada abstract se preprocesa y se convierte en su vector TF-IDF (el mismo de la similitud). La distancia entre
            dos abstracts es 1 menos su coseno: 0 si son iguales, 1 si no comparten ninguna palabra importante. Se
            calcula una matriz de {n} × {n}, solo la mitad de arriba porque es simétrica ({(n * (n - 1)) / 2} pares).
          </p>
          <Formula>d(i, j) = 1 − cos(vᵢ, vⱼ)</Formula>
          <Codigo archivo="clustering/distancias.py" funcion="matriz_distancias" />
        </Desplegable>
        <Desplegable titulo="Los tres criterios" resumen="Cómo se mide la distancia entre dos grupos">
          <p className="max-w-3xl text-sm leading-relaxed">
            Al empezar, cada artículo es su propio grupo. En cada paso se comparan todos los pares de grupos y se unen
            los dos más cercanos, hasta que queda uno solo ({n - 1} uniones).
          </p>
          <div className="grid gap-2 md:grid-cols-3">
            <Formula>single: mín d(x, y)</Formula>
            <Formula>complete: máx d(x, y)</Formula>
            <Formula>average: Σ d(x, y) / (|Cᵢ|·|Cⱼ|)</Formula>
          </div>
          <p className="text-sm text-tinta-suave">x recorre los artículos del grupo Cᵢ e y los del grupo Cⱼ.</p>
          <Codigo archivo="clustering/jerarquico.py" funcion="clustering_jerarquico, distancia_entre_grupos" />
          <p className="mt-2 text-sm text-tinta-suave">
            Complejidad: n − 1 pasos, y en cada uno se comparan todos los pares de grupos → O(n³).
          </p>
        </Desplegable>
        <Desplegable titulo="Correlación cofenética" resumen="La métrica que decide qué criterio es más coherente">
          <p className="max-w-3xl text-sm leading-relaxed">
            La distancia cofenética entre dos artículos es la altura del dendrograma donde quedan juntos por primera vez.
            Se compara con la distancia real usando la correlación de Pearson sobre todos los pares: si da 1, el árbol
            respeta exactamente las distancias originales.
          </p>
          <Formula>r = Σ (x − x̄)(y − ȳ) / √( Σ (x − x̄)² · Σ (y − ȳ)² )</Formula>
          <p className="font-mono text-sm leading-7">
            {datos.criterios.map((c) => (
              <span key={c.criterio} className="block">
                {NOMBRES[c.criterio].titulo}: {c.cofenetica.toFixed(4)}
              </span>
            ))}
          </p>
          {mejor && (
            <p className="mt-2 text-sm text-tinta">
              {NOMBRES[mejor.criterio].titulo} tiene la correlación más alta, así que su árbol es el que mejor representa
              las distancias reales entre los abstracts.
            </p>
          )}
          <Codigo archivo="clustering/metrica.py" funcion="matriz_cofenetica, correlacion_pearson" />
        </Desplegable>
      </section>
    </>
  )
}
