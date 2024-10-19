# fastapi-async

uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000


ab -v 2 -p ./data/note.json -T application/json -n 100 -c 10 http://localhost:8000/notes/sync/

ab -v 2 -p ./data/note.json -T application/json -n 100 -c 10 http://localhost:8000/notes/
