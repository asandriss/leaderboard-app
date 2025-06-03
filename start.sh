#!/usr/bin/env bash

# Stop on errors
set -e

echo "🔁 Starting leaderboard app..."

# 1. Activate Python virtualenv
echo "🐍 Activating virtualenv..."
source .venv/bin/activate

# 2. Start Redis (if using Docker)
# if ! docker ps | grep -q redis; then
#   echo "🧱 Starting Redis container..."
#   docker run -d --name leaderboard-redis -p 6379:6379 redis:7-alpine
# else
#   echo "🔁 Redis already running"
# fi

# 3. Start Flask backend
echo "🚀 Starting backend..."
# FLASK_APP=backend/app.py flask run > backend.log 2>&1 &
FLASK_APP=backend/app.py FLASK_DEBUG=1 flask run --reload --host=0.0.0.0 --port=5000 > backend.log 2>&1 &

# 4. Start React frontend
echo "🌐 Starting frontend..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
cd ..

echo "✅ App started at:"
echo "🔸 Frontend: http://localhost:5173"
echo "🔸 Backend:  http://localhost:5000"
