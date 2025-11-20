import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { convertRegex, withAbsoluteResourceUrls } from '../utils/api'

const examplePatterns = [
  {
    pattern: 'ab(b|c)*d+',
    description: 'alternation and repetition',
  },
  {
    pattern: '(a|b)*c',
    description: 'simple alternation with star',
  },
  {
    pattern: 'a+b*',
    description: 'one or more, zero or more',
  },
]

const generateId = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }

  return `${Date.now()}-${Math.random().toString(16).slice(2)}`
}

const getHistory = () => {
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

const saveHistory = (entries) => {
  if (typeof window === 'undefined') {
    return
  }

  window.localStorage.setItem('history', JSON.stringify(entries))
}

const InputPage = () => {
  const [regex, setRegex] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (event) => {
    event.preventDefault()

    if (!regex.trim()) {
      setError('Please enter a regular expression.')
      return
    }

    try {
      setLoading(true)
      setError('')

      const payload = await convertRegex(regex.trim())

      const entry = withAbsoluteResourceUrls({
        id: generateId(),
        regex: regex.trim(),
        ...payload,
        date: new Date().toISOString(),
      })

      const history = getHistory()
      saveHistory([entry, ...history])

      navigate(`/result/${entry.id}`)
    } catch (err) {
      const message =
        err.response?.data?.message ??
        err.message ??
        'Conversion failed. Please try again.'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-gradient-to-br from-slate-100 via-slate-100 to-blue-50">
      <div className="mx-auto max-w-5xl px-4 py-14">
        <section className="mb-10 text-center">
          <h1 className="text-3xl font-bold text-slate-800 sm:text-4xl">
            Regex to Automata Converter
          </h1>
          <p className="mt-3 text-base text-slate-600 sm:text-lg">
            Visualize regular expressions as NFA, DFA, and Minimized DFA.
          </p>
        </section>

        <div className="grid gap-8 lg:grid-cols-5">
          <div className="lg:col-span-3">
            <div className="rounded-3xl bg-white p-8 shadow-xl">
              <h2 className="text-xl font-semibold text-slate-800">
                Enter Regular Expression
              </h2>
              <form className="mt-6 space-y-6" onSubmit={handleSubmit}>
                <div>
                  <label
                    className="text-left text-sm font-medium text-slate-600"
                    htmlFor="regex"
                  >
                    Regular Expression
                  </label>
                  <input
                    id="regex"
                    className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4 text-lg text-slate-800 shadow-inner outline-none transition focus:border-blue-400 focus:bg-white focus:ring-2 focus:ring-blue-100"
                    placeholder="e.g., ab(b|c)*d+"
                    value={regex}
                    onChange={(event) => setRegex(event.target.value)}
                    disabled={loading}
                  />
                </div>

                {error ? (
                  <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-600">
                    {error}
                  </div>
                ) : null}

                <div className="flex flex-col gap-3 sm:flex-row">
                  <button
                    type="submit"
                    className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-cyan-500 to-blue-500 px-6 py-3 text-base font-semibold text-white shadow-lg transition hover:from-cyan-600 hover:to-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-200 disabled:cursor-not-allowed disabled:opacity-70"
                    disabled={loading}
                  >
                    {loading ? 'Converting...' : 'Convert to Automata'}
                  </button>
                  <button
                    type="button"
                    className="inline-flex items-center justify-center rounded-full border border-transparent bg-slate-200 px-6 py-3 text-base font-semibold text-slate-700 shadow-inner transition hover:bg-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-200"
                    onClick={() => navigate('/history')}
                  >
                    View History
                  </button>
                </div>
              </form>
            </div>
          </div>

          <aside className="lg:col-span-2">
            <div className="rounded-3xl bg-white p-6 shadow-xl">
              <h3 className="text-lg font-semibold text-slate-800">
                Example Regex Patterns
              </h3>
              <div className="mt-4 space-y-4">
                {examplePatterns.map(({ pattern, description }) => (
                  <button
                    key={pattern}
                    type="button"
                    onClick={() => setRegex(pattern)}
                    className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-left shadow-sm transition hover:border-blue-300 hover:bg-blue-50"
                  >
                    <span className="font-semibold text-blue-600">{pattern}</span>
                    <span className="block text-sm text-slate-500">{description}</span>
                  </button>
                ))}
              </div>
            </div>
          </aside>
        </div>
      </div>
    </div>
  )
}

export default InputPage

