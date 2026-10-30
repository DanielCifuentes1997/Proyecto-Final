// Colores que se usan en los dibujos SVG (mapa de calor y dendrograma), iguales a los de index.css
const PALETA = {
  celdaClara: [242, 245, 246],
  celdaOscura: [15, 94, 110],
  diagonal: '#0B2E3B',
  resalte: '#F2B134',
  ramaSinGrupo: '#9AA9AE',
  grupos: ['#0F5E6E', '#E07A3F', '#7A4FA3', '#2E9C8F', '#C8475B', '#C9A227', '#3D6FB0', '#6B7F86'],
}

export function paleta() {
  return PALETA
}
