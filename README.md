# Regex to Minimised DFA Website

A full-stack web application to convert regular expressions (regex) into NFA, DFA, and minimized DFA, with visualizations and downloadable outputs.

## Features
- **Regex to Automata:** Converts user-input regex to NFA, DFA, and minimized DFA.
- **Visualization:** View and download automata as PNG and JSON.
- **History:** Browse previous conversions.
- **Modern UI:** Built with React, Vite, and TailwindCSS.

---

## Project Structure

```
backend/
  main.py              # Flask API server
  convert.py           # Orchestrates regex → NFA → DFA → MinDFA
  regex_to_nfa.py      # Regex to NFA logic
  nfa_to_dfa.py        # NFA to DFA logic
  minimize_dfa.py      # DFA minimization logic
  graph_render.py      # Renders automata as PNG/JSON
  static/output/       # Stores generated automata files

frontend/
  src/
    pages/             # Main pages (Input, Result, History)
    components/        # UI components (Header, etc.)
    utils/api.js       # API client for backend
  public/              # Static assets
  ... (Vite, Tailwind, ESLint configs)
```

---

## How It Works
1. **User Input:** Enter a regex in the web UI.
2. **API Call:** Frontend sends regex to backend `/convert` endpoint.
3. **Processing:** Backend generates NFA, DFA, MinDFA, saves PNG/JSON outputs.
4. **Results:** Frontend displays automata and provides download links.

---

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 18+

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install flask graphviz
# (Optional) Install other dependencies if needed
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Configuration
- The frontend expects the backend to run at `http://localhost:8000` by default. Adjust `VITE_API_BASE_URL` in `.env` if needed.

---

## License
MIT

