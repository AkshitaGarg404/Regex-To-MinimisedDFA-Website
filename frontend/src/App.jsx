import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Header from './components/Header.jsx'
import HistoryPage from './pages/HistoryPage.jsx'
import InputPage from './pages/InputPage.jsx'
import ResultPage from './pages/ResultPage.jsx'

const App = () => {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen flex-col bg-slate-100">
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<InputPage />} />
            <Route path="/result/:id" element={<ResultPage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
