export default function Encabezado({ titulo, children, acciones }) {
  return (
    <header className="mb-6 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
      <div className="max-w-3xl">
        <h1 className="text-4xl text-tinta">{titulo}</h1>
        {children && <p className="mt-3 text-base leading-relaxed text-tinta-suave">{children}</p>}
      </div>
      {acciones && <div className="shrink-0">{acciones}</div>}
    </header>
  )
}
