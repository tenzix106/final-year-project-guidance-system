# Flask Backend

Minimal Flask backend for auth scaffolding (register/login/me) with JWT.

## Setup

1. Python 3.10+
2. Create virtual env and install deps:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows PowerShell
   pip install -r requirements.txt
   ```
3. Environment variables:
   - Copy `.env.example` to `.env` and set secrets
4. Initialize database (SQLite by default):
   ```bash
   flask --app wsgi db init
   flask --app wsgi db migrate -m "init"
   flask --app wsgi db upgrade
   ```
5. Run server:
   ```bash
   flask --app wsgi run --debug
   ```

## Endpoints

- POST `/api/auth/register` { email, password }
- POST `/api/auth/login` { email, password }
- GET `/api/auth/me` (Authorization: Bearer <token>)
 - POST `/api/ai/generate-topics`

