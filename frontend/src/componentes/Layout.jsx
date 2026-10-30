import { NavLink, Outlet } from 'react-router-dom'
import { Library, GitCompareArrows, Network, TextSearch, Info } from 'lucide-react'
import { useCorpus } from './CorpusContexto.jsx'

const SECCIONES = [
  { ruta: '/', nombre: 'Corpus', icono: Library, fin: true },
  { ruta: '/similitud', nombre: 'Similitud textual', icono: GitCompareArrows },
  { ruta: '/clustering', nombre: 'Agrupamiento', icono: Network },
  { ruta: '/busqueda', nombre: 'Búsqueda de patrones', icono: TextSearch },
  { ruta: '/acerca', nombre: 'Acerca del proyecto', icono: Info },
]

export default function Layout() {
  const { corpus } = useCorpus()
  return (
    <div className="min-h-screen lg:flex">
      <aside className="border-b border-linea bg-white lg:fixed lg:inset-y-0 lg:w-64 lg:border-b-0 lg:border-r">
        <div className="flex h-full flex-col px-5 py-6">
          <div className="mb-8 flex items-center gap-3">
            <img src="/favicon.svg" alt="" className="h-9 w-9" />
            <div>
              <p className="font-serif text-xl leading-tight">BiblioAnálisis</p>
              <p className="text-xs text-tinta-suave">Análisis de Algoritmos 2026-2</p>
            </div>
          </div>
          <nav className="flex gap-1 overflow-x-auto lg:flex-col">
            {SECCIONES.map(({ ruta, nombre, icono, fin }) => {
              const Icono = icono
              return (
              <NavLink
                key={ruta}
                to={ruta}
                end={fin}
                className={({ isActive }) =>
                  'flex shrink-0 items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors ' +
                  (isActive ? 'bg-azul-claro font-medium text-azul' : 'text-tinta-suave hover:bg-papel hover:text-tinta')
                }
              >
                <Icono size={18} strokeWidth={1.8} aria-hidden="true" />
                {nombre}
              </NavLink>
              )
            })}
          </nav>
          <div className="mt-auto hidden border-t border-linea pt-4 text-xs leading-relaxed text-tinta-suave lg:block">
            {corpus ? (
              <p>
                Trabajando con <span className="font-medium text-tinta">{corpus.articulos.length} artículos</span>.
                Todo se recalcula al subir o eliminar un PDF.
              </p>
            ) : (
              <p>Conectando con el servidor…</p>
            )}
          </div>
        </div>
      </aside>
      <main className="flex-1 lg:ml-64">
        <div className="mx-auto max-w-6xl px-5 py-8 lg:px-10 lg:py-10">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
