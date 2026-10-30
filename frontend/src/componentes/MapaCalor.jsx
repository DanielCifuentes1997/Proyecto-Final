import { useState } from 'react'

const COLORES_GRUPO = ['#23497A', '#6B93BD', '#B08A3E', '#7E8C9B', '#3F7C8C', '#9C6B5E']

export function colorGrupo(grupo) {
  return COLORES_GRUPO[grupo % COLORES_GRUPO.length]
}

// mezcla lineal entre el papel y el azul según el valor (0 a 1)
function colorCelda(valor) {
  const a = [245, 247, 250]
  const b = [35, 73, 122]
  const c = []
  for (let k = 0; k < 3; k++) c.push(Math.round(a[k] + (b[k] - a[k]) * valor))
  return 'rgb(' + c.join(',') + ')'
}

export default function MapaCalor({ mapa, titulos, seleccion, alElegirPar }) {
  const [foco, setFoco] = useState(null)
  const n = mapa.ids.length
  let maximo = 0
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      if (i !== j && mapa.similitud[i][j] > maximo) maximo = mapa.similitud[i][j]
    }
  }
  if (maximo === 0) maximo = 1
  const celda = n <= 20 ? 22 : n <= 40 ? 13 : 8
  const margen = 34

  return (
    <div>
      <div className="overflow-x-auto">
        <svg
          width={margen + n * celda + 4}
          height={margen + n * celda + 4}
          role="img"
          aria-label="Mapa de calor de similitud TF-IDF entre los artículos"
        >
          {mapa.ids.map((id, i) => (
            <g key={'f' + id}>
              <rect x={margen - 10} y={margen + i * celda + 2} width={6} height={celda - 4} rx={1} fill={colorGrupo(mapa.grupos[i])} />
              <text x={margen - 14} y={margen + i * celda + celda / 2 + 4} textAnchor="end" className="fill-tinta-suave font-mono text-[10px]">
                {id}
              </text>
              <text x={margen + i * celda + celda / 2} y={margen - 14} textAnchor="middle" className="fill-tinta-suave font-mono text-[10px]">
                {id}
              </text>
              <rect x={margen + i * celda + 2} y={margen - 10} width={celda - 4} height={6} rx={1} fill={colorGrupo(mapa.grupos[i])} />
            </g>
          ))}
          {mapa.similitud.map((fila, i) =>
            fila.map((valor, j) => {
              const activa = !foco || foco.i === i || foco.j === j
              const elegida = seleccion && seleccion.includes(mapa.ids[i]) && seleccion.includes(mapa.ids[j]) && i !== j
              return (
                <rect
                  key={i + '-' + j}
                  x={margen + j * celda}
                  y={margen + i * celda}
                  width={celda - 1}
                  height={celda - 1}
                  fill={i === j ? '#1B2B44' : colorCelda(Math.min(valor / maximo, 1))}
                  stroke={elegida ? '#E8B931' : 'none'}
                  strokeWidth={elegida ? 2 : 0}
                  opacity={activa ? 1 : 0.55}
                  className={i !== j ? 'cursor-pointer' : ''}
                  onMouseEnter={() => setFoco({ i, j, valor })}
                  onClick={() => i !== j && alElegirPar && alElegirPar(mapa.ids[i], mapa.ids[j])}
                />
              )
            }),
          )}
        </svg>
      </div>
      <div className="mt-3 min-h-[3.5rem] text-sm text-tinta-suave" aria-live="polite">
        {foco && foco.i !== foco.j ? (
          <p>
            <span className="font-medium text-tinta">
              Artículo {mapa.ids[foco.i]} y artículo {mapa.ids[foco.j]}
            </span>
            : similitud TF-IDF de <span className="font-mono text-tinta">{foco.valor.toFixed(4)}</span>.
            <br />
            <span className="line-clamp-1">{titulos[mapa.ids[foco.i]]}</span>
          </p>
        ) : (
          <p>Pase el cursor sobre una casilla para ver el par. Haga clic para compararlo con los 6 algoritmos.</p>
        )}
      </div>
    </div>
  )
}
