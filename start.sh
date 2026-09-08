#!/bin/bash

cleanup(){
	echo ""
	echo "Stopping services..."
	kill 0
}

trap cleanup SIGINT SIGTERM

echo "Starting Django..."
(
	cd services/Django
	./environment/Scripts/python manage.py runserver
) &

echo "Starting Node..."
(
	cd services/Node
	npm run dev
) &

echo "Starting FastAPI..."
(
	cd services/FastAPI
	if [ -f "app/main.py" ]; then
		./fastAPIenv/Scripts/python -m uvicorn app.main:app --port 8002 --reload
	elif [ -f "main.py" ]; then
		./fastAPIenv/Scripts/python -m uvicorn main:app --port 8002 --reload
	else
		echo "Notice: FastAPI app/main.py not found. Skipping FastAPI server."
	fi
) &

echo "Django + Node + FastAPI running..."

wait