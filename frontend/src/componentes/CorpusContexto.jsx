import { createContext, useCallback, useContext, useEffect, useState } from 'react'
import { api } from '../api.js'

const Contexto = createContext(null)

export function CorpusProvider({ children }) {
  const [corpus, setCorpus] = useState(null)
  const [mapa, setMapa] = useState(null)
  const [error, setError] = useState(null)
  const [version, setVersion] = useState(0)

  const recargar = useCallback(async () => {
    try {
      const [c, m] = await Promise.all([api.corpus(), api.mapa()])
      setCorpus(c)
      setMapa(m)
      setError(null)
      setVersion((v) => v + 1)
    } catch (e) {
      setError(e.message)
    }
  }, [])

  useEffect(() => {
    recargar()
  }, [recargar])

  return (
    <Contexto.Provider value={{ corpus, mapa, error, recargar, version }}>
      {children}
    </Contexto.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export function useCorpus() {
  return useContext(Contexto)
}
