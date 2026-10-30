import { useMemo, useState } from 'react'
import { paleta } from './paleta.js'

export function colorDeGrupo(k) {
  const g = paleta().grupos
  return g[k % g.length]
}

// Igual que cortar_en_grupos en Python: aplico las primeras n-k fusiones
export function gruposAlCortar(fusiones, n, k) {
  const miembros = {}
  for (let i = 0; i < n; i++) miembros[i] = [i]
  let siguiente = n
  const activos = new Set([...Array(n).keys()])
  for (let paso = 0; paso < n - k; paso++) {
    const { a, b } = fusiones[paso]
    miembros[siguiente] = [...miembros[a], ...miembros[b]]
    activos.delete(a)
    activos.delete(b)
    activos.add(siguiente)
    siguiente++
  }
  const grupoDe = new Array(n).fill(0)
  const nodoGrupo = {}
  let numero = 0
  for (const nodo of activos) {
    nodoGrupo[nodo] = numero
    for (const doc of miembros[nodo]) grupoDe[doc] = numero
    numero++
  }
  return { grupoDe, miembros }
}

export default function Dendrograma({ criterio, etiquetas, k }) {
  const [foco, setFoco] = useState(null)
  const n = etiquetas.length
  const ancho = 900
  const alto = 380
  const margen = { izq: 52, der: 16, arriba: 16, abajo: 46 }

  const dibujo = useMemo(() => {
    const { fusiones, orden } = criterio
    const paso = (ancho - margen.izq - margen.der) / n
    const x = {}
    const h = {}
    orden.forEach((doc, pos) => {
      x[doc] = margen.izq + paso * pos + paso / 2
      h[doc] = 0
    })
    let minimo = Infinity
    let maximo = 0
    fusiones.forEach((f) => {
      minimo = Math.min(minimo, f.distancia)
      maximo = Math.max(maximo, f.distancia)
    })
    const base = Math.max(0, minimo - 0.05)
    const tope = Math.min(1, maximo + 0.01)
    const y = (d) => margen.arriba + (alto - margen.arriba - margen.abajo) * (1 - (d - base) / (tope - base || 1))
    const { grupoDe } = gruposAlCortar(fusiones, n, k)
    // grupo de cada nodo interno: si sus hijos son del mismo grupo y está por debajo del corte
    const grupoNodo = {}
    for (let i = 0; i < n; i++) grupoNodo[i] = grupoDe[i]
    const lineas = []
    fusiones.forEach((f, idx) => {
      const id = n + idx
      x[id] = (x[f.a] + x[f.b]) / 2
      h[id] = f.distancia
      const debajoDelCorte = idx < n - k
      const mismo = grupoNodo[f.a] !== null && grupoNodo[f.a] === grupoNodo[f.b]
      grupoNodo[id] = debajoDelCorte && mismo ? grupoNodo[f.a] : null
      lineas.push({ id, idx, f, x1: x[f.a], x2: x[f.b], y1: y(h[f.a] || base), y2: y(h[f.b] || base), yf: y(f.distancia), grupo: grupoNodo[id] })
    })
    const corte = k > 1 && k <= n - 1 ? (fusiones[n - k - 1].distancia + fusiones[n - k].distancia) / 2 : null
    const marcas = []
    for (let v = Math.ceil(base * 20) / 20; v <= tope + 1e-9; v += 0.05) marcas.push(v)
    return { x, y, base, lineas, grupoDe, corte, marcas, orden }
  }, [criterio, n, k])

  const { x, y, base, lineas, grupoDe, corte, marcas, orden } = dibujo
  const titulo = (doc) => etiquetas[doc]

  return (
    <div>
      <div className="overflow-x-auto">
        <svg viewBox={'0 0 ' + ancho + ' ' + alto} className="w-full min-w-[640px]" role="img" aria-label="Dendrograma">
          {marcas.map((v) => (
            <g key={v}>
              <line x1={margen.izq} x2={ancho - margen.der} y1={y(v)} y2={y(v)} stroke="#E6EBF1" />
              <text x={margen.izq - 8} y={y(v) + 4} textAnchor="end" className="fill-tinta-suave font-mono text-[10px]">
                {v.toFixed(2)}
              </text>
            </g>
          ))}
          {corte !== null && (
            <g>
              <line x1={margen.izq} x2={ancho - margen.der} y1={y(corte)} y2={y(corte)} stroke={paleta().resalte} strokeWidth={1.5} strokeDasharray="5 4" />
              <text x={ancho - margen.der} y={y(corte) - 5} textAnchor="end" className="fill-[#8a6a12] text-[11px]">
                corte en {k} grupos
              </text>
            </g>
          )}
          {lineas.map((l) => {
            const color = l.grupo === null ? paleta().ramaSinGrupo : colorDeGrupo(l.grupo)
            const resaltada = foco && foco.tipo === 'fusion' && foco.idx === l.idx
            return (
              <g key={l.id} onMouseEnter={() => setFoco({ tipo: 'fusion', idx: l.idx, f: l.f })} className="cursor-default">
                <path
                  d={'M' + l.x1 + ' ' + l.y1 + ' V' + l.yf + ' H' + l.x2 + ' V' + l.y2}
                  fill="none"
                  stroke={color}
                  strokeWidth={resaltada ? 3 : 1.6}
                />
                <path d={'M' + l.x1 + ' ' + l.yf + ' H' + l.x2} stroke="transparent" strokeWidth={10} />
              </g>
            )
          })}
          {orden.map((doc) => (
            <g key={'h' + doc} onMouseEnter={() => setFoco({ tipo: 'hoja', doc })}>
              <circle cx={x[doc]} cy={y(base)} r={3.5} fill={colorDeGrupo(grupoDe[doc])} />
              <text x={x[doc]} y={y(base) + 18} textAnchor="middle" className="fill-tinta font-mono text-[11px]">
                {titulo(doc).id}
              </text>
              <rect x={x[doc] - 12} y={y(base) - 8} width={24} height={36} fill="transparent" />
            </g>
          ))}
        </svg>
      </div>
      <div className="min-h-[3rem] text-sm text-tinta-suave" aria-live="polite">
        {foco && foco.tipo === 'hoja' && (
          <p>
            <span className="font-medium text-tinta">Artículo {titulo(foco.doc).id}:</span> {titulo(foco.doc).titulo}
          </p>
        )}
        {foco && foco.tipo === 'fusion' && (
          <p>
            <span className="font-medium text-tinta">Fusión {foco.idx + 1}</span> a distancia{' '}
            <span className="font-mono text-tinta">{foco.f.distancia.toFixed(4)}</span>: se forma un grupo de {foco.f.tamano} artículos.
          </p>
        )}
        {!foco && <p>Pase el cursor por un número para ver el título, o por una unión para ver su distancia.</p>}
      </div>
    </div>
  )
}
