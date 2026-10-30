import { ChevronDown } from 'lucide-react'

export default function Desplegable({ titulo, resumen, children, abierto = false }) {
  return (
    <details open={abierto} className="group rounded-lg border border-linea bg-white">
      <summary className="flex cursor-pointer list-none items-center justify-between gap-4 px-5 py-4">
        <span>
          <span className="block font-serif text-xl">{titulo}</span>
          {resumen && <span className="mt-0.5 block text-sm text-tinta-suave">{resumen}</span>}
        </span>
        <ChevronDown size={18} className="shrink-0 text-tinta-suave transition-transform group-open:rotate-180" aria-hidden="true" />
      </summary>
      <div className="border-t border-linea px-5 py-5">{children}</div>
    </details>
  )
}

export function Formula({ children }) {
  return (
    <p className="my-3 inline-block rounded-md border border-linea bg-papel px-4 py-2 font-mono text-sm text-tinta">{children}</p>
  )
}

export function Codigo({ archivo, funcion }) {
  return (
    <p className="mt-4 text-sm text-tinta-suave">
      En el código: <span className="font-mono text-tinta">{archivo}</span>, función{' '}
      <span className="font-mono text-tinta">{funcion}</span>
    </p>
  )
}
