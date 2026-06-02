#!/usr/bin/env bash
set -euo pipefail

echo "=== Grant-O-Matic Setup ==="

# Backend
echo ""
echo "--- Backend (Python) ---"
cd api
python -m pip install -q -r requirements.txt
echo "Backend dependencies installed."
echo "To start: cd api && python main.py"
cd ..

# Frontend
echo ""
echo "--- Frontend (React) ---"
cd frontend
npm install --silent
echo "Frontend dependencies installed."
echo "To start: cd frontend && npm run dev"
cd ..

echo ""
echo "=== Setup complete! ==="
echo ""
echo "To run the full app, open TWO terminals:"
echo "  Terminal 1: cd api && python main.py"
echo "  Terminal 2: cd frontend && npm run dev"
echo ""
echo "Then open http://localhost:5173 in your browser."
