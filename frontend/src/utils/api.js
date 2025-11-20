import axios from 'axios'

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

const ABSOLUTE_URL_REGEX = /^https?:\/\//i
const STATIC_SEGMENT = /[/\\]static[/\\]output[/\\]/i

const normaliseStaticPath = (path) => {
  if (!path || typeof path !== 'string') {
    return path
  }

  const index = path.search(STATIC_SEGMENT)
  if (index === -1) {
    return path
  }

  const segmentStart = path.slice(index).replace(/\\/g, '/')
  return segmentStart.startsWith('/static/')
    ? segmentStart
    : `/static/${segmentStart.replace(/^static\//, '')}`
}
const IMAGE_KEYS = ['nfa_img', 'dfa_img', 'mindfa_img']
const RESOURCE_KEYS = [...IMAGE_KEYS, 'nfa_json', 'dfa_json', 'mindfa_json']

const ensureImageExtension = (path) => {
  if (!path || typeof path !== 'string') {
    return path
  }

  if (path.endsWith('.png.png')) {
    return path
  }

  if (path.endsWith('.png')) {
    return `${path}.png`
  }

  return path
}

export const toAbsoluteUrl = (path) => {
  if (!path || typeof path !== 'string') {
    return path
  }

  const normalised = normaliseStaticPath(path)

  if (ABSOLUTE_URL_REGEX.test(normalised)) {
    return normalised
  }

  if (normalised.startsWith('/')) {
    return `${API_BASE_URL.replace(/\/$/, '')}${normalised}`
  }

  try {
    const base = API_BASE_URL.endsWith('/') ? API_BASE_URL : `${API_BASE_URL}/`
    return new URL(normalised, base).toString()
  } catch {
    return normalised
  }
}

export const withAbsoluteResourceUrls = (data) => {
  if (!data || typeof data !== 'object') {
    return data
  }

  return RESOURCE_KEYS.reduce((acc, key) => {
    if (key in acc) {
      const value =
        IMAGE_KEYS.includes(key) ? ensureImageExtension(acc[key]) : acc[key]
      acc[key] = toAbsoluteUrl(value)
    }
    return acc
  }, { ...data })
}

export const convertRegex = async (regex) => {
  const response = await apiClient.post('/convert', { regex })
  return withAbsoluteResourceUrls(response.data)
}

export default apiClient

