# Development Setup Guide

## Quick Start Options

### Option 1: Single Command (Recommended)
```bash
# Start all services at once
npm run start:all
```
This starts:
- Frontend (Vue.js) on http://localhost:3000
- Express Backend (AI proxy) on http://localhost:3001  
- Flask Backend (Auth/DB) on http://localhost:5000

### Option 2: Express Backend Only (AI features only)
```bash
# Start frontend + Express backend (most common for development)
npm run dev:express
```

### Option 3: Using Scripts
**Windows Batch:**
```cmd
start-all.bat
```

**PowerShell:**
```powershell
.\start-all.ps1
```

### Option 4: Manual (Original way)
```bash
# Terminal 1 - Frontend
npm run dev

# Terminal 2 - Express Backend  
cd backend
npm run dev

# Terminal 3 - Flask Backend (optional)
cd backend_flask
flask --app wsgi run --debug
```

## Available NPM Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Frontend only (Vue.js) |
| `npm run dev:express` | Frontend + Express backend |
| `npm run dev:all` | All three services |
| `npm run start:all` | All three services with colored output |
| `npm run backend:express` | Express backend only |
| `npm run backend:flask` | Flask backend only |

## Service URLs

- **Frontend**: http://localhost:3000 (Vue.js + Vite)
- **Express API**: http://localhost:3001 (AI proxy)
- **Flask API**: http://localhost:5000 (Auth + Database)

## Notes

- The **Express backend is required** for AI functionality (Gemini API proxy)
- The **Flask backend is optional** unless you need user authentication
- All services have auto-reload enabled for development
- Use `Ctrl+C` to stop all services when using concurrent mode