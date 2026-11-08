# Kathā-Kosh

**A digital archive for India's living cultural heritage.**

Kathā-Kosh is an AI-powered platform for preserving and discovering regional folk stories, traditional crafts, oral histories, folk art, and cultural traditions from across India.

---

## Features

- **Semantic Search** — Find heritage items using natural language queries powered by vector embeddings
- **Image Search** — Upload an image to find visually similar artifacts in the archive
- **Cultural Archive** — Browse 25+ documented heritage entries from 15+ Indian states
- **Contribution Portal** — Submit new stories, crafts, and cultural knowledge
- **AI Categorization** — Automatic category and tag suggestions for new contributions
- **Interactive Map** — Explore heritage entries by region
- **Story Reader** — Distraction-free reading experience for folk stories
- **Admin Panel** — Moderate contributions and manage the archive

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Tailwind CSS, Framer Motion |
| Backend | Python, FastAPI, SQLAlchemy |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Search | FAISS vector store + Sentence Transformers |
| Image AI | CLIP (OpenAI) with fallback |
| Auth | JWT tokens |

---

## Quick Start

### Prerequisites

- Node.js 18+ 
- Python 3.10+
- Git

### 1. Clone the repository

```bash
git clone <repo-url>
cd katha-kosh
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Optional: Install AI dependencies for real vector search
pip install sentence-transformers faiss-cpu
# For image search:
pip install transformers torch torchvision

# Copy environment file
copy .env.example .env

# Seed the database with sample data
python seed_data.py

# Start the backend
uvicorn app.main:app --reload --port 8000
```

The backend will be available at: http://localhost:8000

API documentation: http://localhost:8000/docs

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at: http://localhost:5173

---

## Production Setup with Docker

```bash
# Start all services
docker-compose up -d

# Seed the database
docker-compose exec backend python seed_data.py
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./katha_kosh.db` | Database connection string |
| `SECRET_KEY` | (required) | JWT signing key |
| `UPLOAD_DIR` | `uploads` | Directory for uploaded files |

---

## AI Search Architecture

```
Text Query → Sentence Transformers → 384-dim vector → FAISS → Ranked Results
                       ↓ (if unavailable)
               SQL LIKE fallback search

Image Upload → CLIP Model → 512-dim vector → FAISS → Similar Artifacts
                   ↓ (if unavailable)
          Hash-based fallback for demo
```

The AI components are designed to degrade gracefully:
- If `sentence-transformers` is not installed, falls back to keyword search
- If `faiss-cpu` is not installed, vector store is disabled
- If CLIP is not available, image search uses a demo fallback

Install the AI dependencies for full functionality:
```bash
pip install sentence-transformers faiss-cpu transformers torch
```

---

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/items` | GET | List heritage items (supports filters) |
| `/api/items/{id}` | GET | Get single item |
| `/api/items` | POST | Create new item |
| `/api/search/text` | POST | Semantic text search |
| `/api/search/image` | POST | Image similarity search |
| `/api/contributions` | GET | List contributions |
| `/api/contributions` | POST | Submit contribution |
| `/api/contributions/{id}/approve` | POST | Approve (admin) |
| `/api/ai/categorize` | POST | AI category suggestion |
| `/api/regions` | GET | List regions |
| `/api/categories` | GET | List categories |
| `/api/admin/stats` | GET | Archive statistics |
| `/api/auth/register` | POST | Register user |
| `/api/auth/login` | POST | Login |
| `/api/auth/me` | GET | Current user |

---

## Project Structure

```
katha-kosh/
├── frontend/
│   └── src/
│       ├── components/      # Reusable UI components
│       ├── pages/           # Page components
│       ├── data/            # Sample data (fallback)
│       ├── services/        # API client
│       ├── hooks/           # Custom React hooks
│       └── context/         # React context
├── backend/
│   └── app/
│       ├── models/          # SQLAlchemy models
│       ├── schemas/         # Pydantic schemas
│       ├── routes/          # API route handlers
│       ├── services/        # Business logic
│       ├── embeddings/      # Text + image embedders
│       └── vector_store/    # FAISS vector store
├── data/
│   └── sample_heritage_data.json
├── docker-compose.yml
└── README.md
```

---

## Contributing

Kathā-Kosh is designed to be extended. To add new heritage entries:
1. Use the Contribution Portal at `/contribute`
2. Or directly via the API: `POST /api/contributions`
3. Admin review at `/admin`

---

## Heritage Categories

| Category | Description |
|----------|-------------|
| Folk Story | Oral and written traditional narratives |
| Craft | Traditional handmade objects and processes |
| Folk Art | Visual art forms with regional traditions |
| Textile | Weaving, embroidery, and fabric traditions |
| Pottery | Clay and ceramic crafts |
| Woodwork | Carving, lacquerware, wooden crafts |
| Metalwork | Bell-metal, brass, silver inlay crafts |
| Dance | Traditional and folk dance forms |
| Music | Folk songs, instruments, oral music |
| Ritual | Ceremonial and religious practices |
| Oral History | Documented community memories |

---

## License

MIT License — See LICENSE file.

---

*Kathā-Kosh — Preserving the stories that should not disappear.*

