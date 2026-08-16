#!/usr/bin/env bash
echo "Starting EngageResolve Development Stack..."
cd backend && export PYTHONPATH=. && python run.py --seed &
BACKEND_PID=$!

cd ../frontend && npm run web &
FRONTEND_PID=$!

echo "Dev stack started!"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:8081"
wait $BACKEND_PID $FRONTEND_PID
