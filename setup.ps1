Write-Host "=== Grant-O-Matic Setup ===" -ForegroundColor Cyan

# Backend
Write-Host "`n--- Backend (Python) ---" -ForegroundColor Yellow
Push-Location api
pip install -q -r requirements.txt
Write-Host "Backend dependencies installed."
Write-Host "To start: cd api && python main.py"
Pop-Location

# Frontend
Write-Host "`n--- Frontend (React) ---" -ForegroundColor Yellow
Push-Location frontend
npm install --silent
Write-Host "Frontend dependencies installed."
Write-Host "To start: cd frontend && npm run dev"
Pop-Location

Write-Host "`n=== Setup complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "To run the full app, open TWO terminals:"
Write-Host "  Terminal 1: cd api && python main.py"
Write-Host "  Terminal 2: cd frontend && npm run dev"
Write-Host ""
Write-Host "Then open http://localhost:5173 in your browser."
