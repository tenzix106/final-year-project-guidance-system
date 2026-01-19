# FYP Guidance System - Start All Services
Write-Host "Starting FYP Guidance System - All Services" -ForegroundColor Green
Write-Host ""
Write-Host "Services will be available at:" -ForegroundColor Yellow
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "  Express Backend: http://localhost:3001" -ForegroundColor Yellow  
Write-Host "  Flask Backend: http://localhost:5000" -ForegroundColor Magenta
Write-Host ""
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Red
Write-Host ""

# Start all services using concurrently
npm run start:all