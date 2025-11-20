import { Link, NavLink } from 'react-router-dom'

const Header = () => {
  return (
    <header className="bg-white shadow-sm">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
        <Link to="/" className="text-xl font-semibold text-slate-800">
          Regex to Automata Converter
        </Link>
        <nav className="flex items-center gap-4 text-sm font-medium text-slate-600">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `rounded-full px-3 py-1 transition-colors ${
                isActive ? 'bg-blue-100 text-blue-600' : 'hover:text-blue-600'
              }`
            }
          >
            Home
          </NavLink>
          <NavLink
            to="/history"
            className={({ isActive }) =>
              `rounded-full px-3 py-1 transition-colors ${
                isActive ? 'bg-blue-100 text-blue-600' : 'hover:text-blue-600'
              }`
            }
          >
            History
          </NavLink>
        </nav>
      </div>
    </header>
  )
}

export default Header



// Authors- Abhyudaya Tak, Akshita Garg