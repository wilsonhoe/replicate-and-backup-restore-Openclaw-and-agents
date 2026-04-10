import json
import urllib.request
import sys

data = {
    "examId": "exam-07b9cbc9",
    "hash": "1bd84805b046562317f8ed8e32333c511e1ff5954e25aeaa078923e06c1036ca",
    "answers": [
        {"questionId": "too-43", "answer": "A"},
        {"questionId": "too-22", "answer": """**docker-compose.yml**
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:16
    env_file: .env
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - '5432:5432'
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U $${POSTGRES_USER}']
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

  redis:
    image: redis:7
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ['CMD', 'redis-cli', 'ping']
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

  minio:
    image: minio/minio:latest
    command: server /data --console-address ':9001'
    env_file: .env
    volumes:
      - minio_data:/data
    ports:
      - '9000:9000'
      - '9001:9001'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:9000/minio/health/live']
      interval: 30s
      timeout: 20s
      retries: 3
    networks:
      - backend

  mailhog:
    image: mailhog/mailhog
    ports:
      - '1025:1025'
      - '8025:8025'
    networks:
      - backend

  backend:
    build: ./backend
    env_file: .env
    volumes:
      - ./backend:/app
    ports:
      - '8000:8000'
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      minio:
        condition: service_healthy
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - backend
      - frontend

  worker:
    build: ./backend
    env_file: .env
    volumes:
      - ./backend:/app
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: celery -A tasks worker --loglevel=info
    networks:
      - backend

  frontend:
    build: ./frontend
    env_file: .env
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - '3000:3000'
    depends_on:
      - backend
    command: npm run dev
    networks:
      - frontend

  pgadmin:
    image: dpage/pgadmin4
    env_file: .env
    ports:
      - '8080:80'
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - backend

volumes:
  postgres_data:
  redis_data:
  minio_data:
  pgadmin_data:

networks:
  backend:
  frontend:
```
**Note:** Assumes backend/Dockerfile (FastAPI + uvicorn, celery), frontend/Dockerfile (Next.js). Backend connects to postgres/redis/minio via backend network. Frontend to backend via frontend/backend networks.

**.env.example**
```
POSTGRES_USER=dev
POSTGRES_PASSWORD=devpass
POSTGRES_DB=appdb
REDIS_URL=redis://redis:6379
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin
CELERY_BROKER_URL=redis://redis:6379/0
```

**init.sql**
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO users (name, email) VALUES
  ('Test User', 'test@example.com');
```

**Makefile**
```makefile
.PHONY: up down logs shell db-reset test

up:
	docker compose up -d

down:
	docker compose down -v

logs:
	docker compose logs -f

shell:
	docker compose exec $(service) sh

db-reset:
	docker compose down postgres
	docker volume rm $$(docker volume ls -q | grep postgres_data)
	docker compose up -d postgres

test:
	docker compose exec backend pytest
	docker compose exec frontend npm test
```
Hot reload via bind mounts. Healthchecks ensure deps ready. Makefile for common ops."""}
    ]
}

url = "https://clawvard.school/api/exam/batch-answer"

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)

with urllib.request.urlopen(req) as response:
    result = response.read().decode('utf-8')
    print(result)
