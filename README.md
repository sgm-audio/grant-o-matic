# Grant-O-Matic

[![CI](https://github.com/your-org/grant-o-matic/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/grant-o-matic/actions/workflows/ci.yml)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue)
![React 18](https://img.shields.io/badge/react-18-61DAFB)
![TypeScript](https://img.shields.io/badge/typescript-5.8-3178C6)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![License](https://img.shields.io/badge/license-MIT-green)
[![Canada](https://img.shields.io/badge/for-Canadian%20Creators-red?logo=icloud&logoColor=white)](https://canadacouncil.ca)

AI-powered grant matching for Canadian artists and creators. Matches your project to the right funding opportunities from FACTOR, Canada Council, provincial arts councils, and more.

---

## One-Click Setup

### Option A: Docker (recommended)
```bash
docker compose up
# Frontend: http://localhost:5173
# API:      http://localhost:8000/docs
```

### Option B: Manual (two terminals)

**Terminal 1 — Backend:**
```bash
cd api
pip install -r requirements.txt
python main.py
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Option C: Platform.sh / Render / Fly.io
Deploy the API as a Uvicorn server (port 8000) and the frontend as static files (`npm run build` → `frontend/dist/`).

---

## How It Works

1. **Describe your project** — tell us what you're making
2. **Get matches** — the engine scores grants by eligibility, project type, keywords, and complexity
3. **Review results** — see match percentage, deadlines, funding amounts, and criteria you meet/miss
4. **Apply with confidence** — use the budget justification generator to strengthen your application

### Supported grant sources
- FACTOR (Juried Sound Recording, Artist Development, etc.)
- Canada Council for the Arts (Explore & Create, Engage & Sustain, etc.)
- Provincial arts councils (OAC, BC Arts Council, etc.)
- Telefilm Canada, CMF, SOCAN Foundation
- Federal and provincial tax credit programs

---

## Architecture

```
┌──────────┐     POST /match     ┌──────────────────┐
│  React   │ ──────────────────→ │  FastAPI backend  │
│  frontend│ ←────────────────── │  port 8000        │
│  :5173   │     JSON response   │  + matching engine│
└──────────┘                     └────────┬─────────┘
                                          │
                                    ┌─────▼─────┐
                                    │  Grant DB  │
                                    │  (JSON)    │
                                    └───────────┘
```

| Layer | Tech |
|-------|------|
| Frontend | React 18, TypeScript 5, Vite 5, Radix UI, TanStack Query, Tailwind CSS |
| Backend | Python 3.12, FastAPI, Uvicorn, Pydantic v2 |
| Matching | Keyword + eligibility scoring engine (no external API needed) |
| Budget gen | Template-based budget justification generator |
| Scrapers | BeautifulSoup + requests (placeholders — extend for live data) |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | API root |
| `GET` | `/health` | Health check with grant count |
| `POST` | `/match` | Match a project to grants |
| `GET` | `/grants` | List all grants |
| `GET` | `/grants/{id}` | Grant detail |
| `POST` | `/scrape` | Trigger grant data scrape |

**`POST /match`** example:
```json
{
  "project_description": "Recording my debut EP as an electronic music producer",
  "artist_type": "individual",
  "residency": "Ontario",
  "genre": "electronic",
  "project_type": "Recording",
  "budget_amount": 15000
}
```

---

## Development

```bash
# Backend tests
cd api && python test_api.py

# Frontend checks
cd frontend && npx tsc --noEmit && npm run lint && npm run build

# Set custom data path
export GRANT_DATA_PATH=/path/to/data
```

---

## Roadmap

- [ ] Live integrated scraping from Canada Council / FACTOR
- [ ] Deadline alert system (email/calendar)
- [ ] Multi-LLM matching via Groq/Anthropic
- [ ] User accounts and saved matches
- [ ] Bilingual (FR/EN) UI
- [ ] SR&ED tax credit eligibility checker

---

## License

MIT — built for Canadian creators, by Canadian creators.
