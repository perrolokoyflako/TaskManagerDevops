# Task Manager API — DevOps Project B3 SR

A REST API for managing tasks, built with **Flask** and **PostgreSQL**, fully containerized with **Docker** and **Docker Compose**, deployed on **Microsoft Azure**.

> SUP DE VINCI — 2025/2026 — B3 SR

---

## Architecture
```
┌─────────────────────────────────────────────┐
│              Docker Compose                 │
│                                             │
│  ┌──────────────┐      ┌─────────────────┐  │
│  │  Flask API   │─────▶│   PostgreSQL    │  │
│  │  (port 5000) │      │   (port 5432)   │  │
│  └──────────────┘      └────────┬────────┘  │
│                                 │           │
│                         postgres_data       │
│                         (named volume)      │
└─────────────────────────────────────────────┘
         │
    taskmanager_network (bridge)
```

- The **API** container handles all HTTP requests (Flask + Gunicorn)
- The **DB** container stores data persistently via a named volume
- Both containers communicate over a **custom bridge network**
- Secrets are managed via a **`.env` file** (never committed to Git)
- The API is deployed on an **Azure VM** and accessible publicly

---

## Quick Start

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

### 1. Clone the repository
```bash
git clone https://github.com/perrolokoyflako/TaskManagerDevops.git
cd TaskManagerDevops
```

### 2. Configure environment variables
```bash
cp .env.example .env
# Edit .env and set your own password
```

### 3. Start all services
```bash
docker compose up -d
```

### 4. Verify everything is running
```bash
docker compose ps
```

### 5. Test the API
```bash
curl http://localhost:5000/health
# → {"status": "ok"}
```

---

## Live Demo

The API is publicly accessible at:
```
http://20.251.146.73:5000
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/:id` | Get one task |
| POST | `/tasks` | Create a task |
| PATCH | `/tasks/:id` | Update a task |
| DELETE | `/tasks/:id` | Delete a task |
| GET | `/stats` | Task statistics |

### Example requests

**Create a task:**
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "My task", "description": "Details here", "priority": "high"}'
```

**Mark a task as done:**
```bash
curl -X PATCH http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

**Get statistics:**
```bash
curl http://localhost:5000/stats
```

---

## Useful Commands
```bash
# Start in background
docker compose up -d

# View logs
docker compose logs -f

# Stop everything
docker compose down

# Full reset (deletes database)
docker compose down -v

# Rebuild after code changes
docker compose up -d --build
```

---

## Project Structure
```
TaskManagerDevops/
├── app/
│   ├── app.py              # Flask application (routes + models)
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Multi-stage Docker build
│   └── .dockerignore       # Files excluded from the image
├── docker-compose.yml      # Service orchestration
├── .env                    # Environment variables (NOT in Git)
├── .env.example            # Template for .env
├── .gitignore
└── README.md
```

---

## Security

- App runs as a **non-root user** inside the container
- Secrets stored in `.env`, excluded from Git via `.gitignore`
- Database port **not exposed** publicly — only the API is
- **Healthcheck** configured on both containers
