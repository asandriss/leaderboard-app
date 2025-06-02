#!/usr/bin/env bash
echo "🛑 Stopping leaderboard app..."
pkill -f "flask run"
pkill -f "vite"
docker stop leaderboard-redis && docker rm leaderboard-redis