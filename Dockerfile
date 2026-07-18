# ── Estágio 1: build do frontend ──────────────────────────────────────────────
FROM node:22-alpine AS frontend
WORKDIR /build
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ── Estágio 2: backend + estáticos ────────────────────────────────────────────
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app/backend
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY backend/ ./
COPY --from=frontend /build/dist /frontend/dist

# O app grava all_files/ e transferencia.db no diretório de trabalho e procura
# o frontend em ../frontend/dist. Com o CWD em /data (volume), os dados
# persistem e ../frontend/dist resolve para /frontend/dist.
WORKDIR /data
EXPOSE 8000
CMD ["uv", "run", "--project", "/app/backend", "uvicorn", "main:app", \
     "--app-dir", "/app/backend", "--host", "0.0.0.0", "--port", "8000"]
