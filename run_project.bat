@echo off
echo Starting EY-teaha-thon Project...

echo Starting Backend (Spring Boot)...
start "Backend Server" cmd /k "cd server && mvn spring-boot:run"

echo Starting Frontend (React)...
start "Frontend Client" cmd /k "cd client && npm run dev"

echo Project started!
echo Backend running on http://localhost:8081
echo Frontend running on http://localhost:5173
pause
