const BASE = import.meta.env.VITE_API_URL || ''

async function pedir(ruta, opciones = {}) {
  const respuesta = await fetch(BASE + ruta, opciones)
  if (!respuesta.ok) {
    let mensaje = 'El servidor respondió con un error (' + respuesta.status + ').'
    try {
      const cuerpo = await respuesta.json()
      if (cuerpo.detail) mensaje = cuerpo.detail
    } catch {
      // la respuesta no trae json
    }
    throw new Error(mensaje)
  }
  return respuesta.json()
}

function enviarJson(ruta, datos) {
  return pedir(ruta, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos),
  })
}

export const api = {
  corpus: () => pedir('/api/corpus'),
  mapa: () => pedir('/api/corpus/mapa'),
  subirPdf: (archivo) => {
    const formulario = new FormData()
    formulario.append('archivo', archivo)
    return pedir('/api/corpus', { method: 'POST', body: formulario })
  },
  eliminar: (id) => pedir('/api/corpus/' + id, { method: 'DELETE' }),
  comparar: (ids) => enviarJson('/api/similitud', { ids }),
  clustering: () => pedir('/api/clustering'),
  buscar: (patron) => enviarJson('/api/busqueda', { patron }),
}
