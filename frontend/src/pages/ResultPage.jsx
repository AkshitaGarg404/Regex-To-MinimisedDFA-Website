import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { withAbsoluteResourceUrls } from '../utils/api'

const loadHistory = () => {
  if (typeof window === 'undefined') {
    return []
  }

  try {
    const entries = JSON.parse(window.localStorage.getItem('history') ?? '[]')
    return Array.isArray(entries)
      ? entries.map((item) => withAbsoluteResourceUrls(item))
      : []
  } catch {
    return []
  }
}

const formatDate = (dateString) => {
  try {
    return new Intl.DateTimeFormat('en', {
      dateStyle: 'medium',
      timeStyle: 'short',
    }).format(new Date(dateString))
  } catch {
    return dateString
  }
}

const ResultPage = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [entry, setEntry] = useState(null)

  useEffect(() => {
    const history = loadHistory()
    const match = history.find((item) => item.id === id)
    setEntry(match ?? null)
  }, [id])

  useEffect(() => {
    if (entry === null) {
      const history = loadHistory()
      if (history.length === 0) {
        return
      }

      if (!history.some((item) => item.id === id)) {
        const timer = setTimeout(() => navigate('/'), 3000)
        return () => clearTimeout(timer)
      }
    }

    return undefined
  }, [entry, id, navigate])

  if (!entry) {
    return (
      <div className="mx-auto flex min-h-[60vh] max-w-3xl flex-col items-center justify-center gap-4 px-4 text-center">
        <h2 className="text-2xl font-semibold text-slate-800">Result not found</h2>
        <p className="max-w-xl text-sm text-slate-600">
          We couldn&apos;t locate this conversion in your history. It may have been
          removed. You will be redirected to the home page shortly.
        </p>
        <button
          type="button"
          className="rounded-full bg-blue-500 px-6 py-2 text-sm font-semibold text-white shadow hover:bg-blue-600"
          onClick={() => navigate('/')}
        >
          Go to Home
        </button>
      </div>
    )
  }

  const downloadLinks = [
    { label: 'Download NFA JSON', href: entry.nfa_json },
    { label: 'Download DFA JSON', href: entry.dfa_json },
    { label: 'Download Minimized DFA JSON', href: entry.mindfa_json },
  ].filter(({ href }) => Boolean(href))

  const visualizations = [
    { title: 'NFA', img: entry.nfa_img },
    { title: 'DFA', img: entry.dfa_img },
    { title: 'Minimized DFA', img: entry.mindfa_img },
  ]

  return (
    <div className="bg-slate-100 py-12">
      <div className="mx-auto max-w-5xl px-4">
        <div className="rounded-3xl bg-white p-8 shadow-xl">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm font-medium uppercase tracking-wide text-blue-500">
                Regular Expression
              </p>
              <h1 className="mt-1 break-words text-2xl font-semibold text-slate-800 sm:text-3xl">
                {entry.regex}
              </h1>
            </div>
            <div className="text-sm text-slate-500">
              Converted on&nbsp;
              <span className="font-medium text-slate-700">{formatDate(entry.date)}</span>
            </div>
          </div>

          <div className="mt-8 grid gap-6 md:grid-cols-3">
            {visualizations.map(({ title, img }) => (
              <div
                key={title}
                className="flex flex-col overflow-hidden rounded-2xl border border-slate-100 bg-slate-50 shadow-sm"
              >
                <div className="border-b border-slate-200 bg-white px-4 py-3">
                  <h2 className="text-lg font-semibold text-slate-800">{title}</h2>
                </div>
                <div className="flex flex-1 items-center justify-center bg-white p-4">
                  {img ? (
                    <img
                      src={img}
                      alt={`${title} visualization`}
                      className="max-h-72 w-full rounded-lg border border-slate-100 object-contain"
                    />
                  ) : (
                    <p className="text-center text-sm text-slate-500">No image available.</p>
                  )}
                </div>
              </div>
            ))}
          </div>

          {downloadLinks.length > 0 ? (
            <div className="mt-8 flex flex-wrap items-center gap-4">
              {downloadLinks.map(({ label, href }) => (
                <a
                  key={label}
                  href={href}
                  className="inline-flex items-center rounded-full border border-blue-200 bg-blue-50 px-4 py-2 text-sm font-semibold text-blue-600 transition hover:border-blue-300 hover:bg-blue-100"
                  download
                >
                  {label}
                </a>
              ))}
            </div>
          ) : null}

          <div className="mt-10 flex flex-wrap items-center gap-3 text-sm font-medium text-blue-600">
            <Link to="/" className="rounded-full bg-blue-500 px-5 py-2 text-white shadow hover:bg-blue-600">
              Convert another regex
            </Link>
            <Link
              to="/history"
              className="rounded-full border border-blue-200 px-5 py-2 text-blue-600 hover:border-blue-300 hover:bg-blue-50"
            >
              View History
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ResultPage

