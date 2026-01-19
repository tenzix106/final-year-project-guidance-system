@echo off
echo Starting FYP Guidance System - All Services
echo.
echo Frontend: http://localhost:3000
echo Express Backend: http://localhost:3001  
echo Flask Backend: http://localhost:5000
echo.
echo Press Ctrl+C to stop all services
echo.

REM Start all services using concurrently
npm run start:all