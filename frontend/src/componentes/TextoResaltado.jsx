// Marca en el texto las palabras que están en el conjunto (misma regla del preprocesamiento: solo letras a-z)
export default function TextoResaltado({ texto, palabras }) {
  const partes = texto.split(/([A-Za-z]+)/)
  return (
    <>
      {partes.map((parte, k) =>
        palabras.has(parte.toLowerCase()) ? (
          <mark key={k} className="marcador">
            {parte}
          </mark>
        ) : (
          <span key={k}>{parte}</span>
        ),
      )}
    </>
  )
}
