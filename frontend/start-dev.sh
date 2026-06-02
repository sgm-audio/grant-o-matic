#!/bin/bash
echo "Starting Grant-O-Matic frontend development server..."
echo "Make sure the backend API is running on http://localhost:8000"
echo "You can start it with: cd ../api && python main.py"
echo ""
npx vite --host 0.0.0.0 --port 5173 --clearScreen=false
