import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import Layout from './componentes/Layout.jsx'
import { CorpusProvider } from './componentes/CorpusContexto.jsx'
import Corpus from './paginas/Corpus.jsx'
import Similitud from './paginas/Similitud.jsx'
import Clustering from './paginas/Clustering.jsx'
import Busqueda from './paginas/Busqueda.jsx'
import Acerca from './paginas/Acerca.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <CorpusProvider>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<Corpus />} />
            <Route path="similitud" element={<Similitud />} />
            <Route path="clustering" element={<Clustering />} />
            <Route path="busqueda" element={<Busqueda />} />
            <Route path="acerca" element={<Acerca />} />
          </Route>
        </Routes>
      </CorpusProvider>
    </BrowserRouter>
  </StrictMode>,
)
