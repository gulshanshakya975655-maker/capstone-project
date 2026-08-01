# TaskFlow

Full-stack task management app built with FastAPI, SQLAlchemy, and vanilla JavaScript.

## Setup

1. Backend: `cd backend`, create venv, `pip install -r requirements.txt`, then `uvicorn main:app --reload`
2. Frontend: `cd backend/frontend`, then `python -m http.server 5500`
3. Open `http://127.0.0.1:5500` in your browser

## Features

- Full CRUD for tasks (create, read, update, delete)
- Projects and users management
- Per-project task statistics
- Custom middleware for request logging
- CORS configured for local frontend
- Responsive dashboard with localStorage caching