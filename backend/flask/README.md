# Flask Backend (coexisting with Node backend)

## Setup

```bash
cd backend/flask
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `SECRET_KEY`, `JWT_SECRET_KEY`, `DATABASE_URL`.

Initialize DB and run:

```bash
flask --app wsgi db init
flask --app wsgi db migrate -m "init"
flask --app wsgi db upgrade
flask --app wsgi run --debug
```

Endpoints:
- POST `/api/auth/register`
- POST `/api/auth/login`
- GET `/api/auth/me`
 - POST `/api/ai/generate-topics`

Environment:
- `.env` (copy from `.env.example`):
  - `SECRET_KEY=...`
  - `JWT_SECRET_KEY=...`
  - `DATABASE_URL=sqlite:///app.db`
  - `GEMINI_API_KEY=your_google_gemini_api_key`

