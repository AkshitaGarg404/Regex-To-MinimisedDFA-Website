import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { withAbsoluteResourceUrls } from '../utils/api'

const loadHistory = () => {
  if (typeof window === 'undefined') {
    return []
  }

  try {
    const entries = JSON.parse(window.localStorage.getItem('history') ?? '[]')
    return Array.isArray(entries)
      ? entries.map((entry) => withAbsoluteResourceUrls(entry))
      : []
  } catch {
    return []
  }
}

const HistoryPage = () => {
  const navigate = useNavigate()
  const [entries, setEntries] = useState([])

  useEffect(() => {
    setEntries(loadHistory())
  }, [])

  const orderedEntries = useMemo(
    () =>
      [...entries].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()),
    [entries],
  )

  if (orderedEntries.length === 0) {
    return (
      <div className="mx-auto flex min-h-[60vh] max-w-3xl flex-col items-center justify-center gap-4 px-4 text-center">
        <h2 className="text-2xl font-semibold text-slate-800">No history yet</h2>
        <p className="max-w-lg text-sm text-slate-600">
          Start by converting a regular expression to see your results here.
        </p>
        <button
          type="button"
          onClick={() => navigate('/')}
          className="rounded-full bg-blue-500 px-6 py-2 text-sm font-semibold text-white shadow hover:bg-blue-600"
        >
          Convert a regex
        </button>
      </div>
    )
  }

  return (
    <div className="bg-slate-100 py-12">
      <div className="mx-auto max-w-5xl px-4">
        <div className="rounded-3xl bg-white p-8 shadow-xl">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h1 className="text-3xl font-semibold text-slate-800">Conversion History</h1>
              <p className="mt-2 text-sm text-slate-500">
                Review your previous regex conversions and revisit their results.
              </p>
            </div>
            <button
              type="button"
              onClick={() => navigate('/')}
              className="rounded-full border border-blue-200 px-5 py-2 text-sm font-semibold text-blue-600 transition hover:border-blue-300 hover:bg-blue-50"
            >
              New conversion
            </button>
          </div>

          <div className="mt-8 divide-y divide-slate-200">
            {orderedEntries.map((entry) => (
              <button
                key={entry.id}
                type="button"
                onClick={() => navigate(`/result/${entry.id}`)}
                className="flex w-full flex-col gap-3 rounded-2xl bg-slate-50 px-5 py-5 text-left shadow-sm transition hover:-translate-y-0.5 hover:bg-blue-50 hover:shadow-md sm:flex-row sm:items-center sm:justify-between"
              >
                <div className="flex-1">
                  <p className="text-sm font-semibold uppercase tracking-wide text-blue-500">
                    {entry.regex}
                  </p>
                  <p className="mt-1 text-xs text-slate-500">
                    {new Date(entry.date).toLocaleString()}
                  </p>
                </div>
                <div className="flex flex-1 flex-col gap-2 text-xs text-slate-500 sm:flex-row sm:justify-end">
                  <span className="inline-flex items-center gap-2 rounded-full bg-white px-3 py-1 shadow-inner">
                    <span className="h-2 w-2 rounded-full bg-green-400" />
                    NFA
                  </span>
                  <span className="inline-flex items-center gap-2 rounded-full bg-white px-3 py-1 shadow-inner">
                    <span className="h-2 w-2 rounded-full bg-sky-400" />
                    DFA
                  </span>
                  <span className="inline-flex items-center gap-2 rounded-full bg-white px-3 py-1 shadow-inner">
                    <span className="h-2 w-2 rounded-full bg-indigo-400" />
                    Min DFA
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default HistoryPage

