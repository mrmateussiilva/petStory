# ---------- builder ----------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev


# ---------- runtime ----------
FROM python:3.12-slim-bookworm

# cria usuário com mesmo UID/GID do deploy (1000)
RUN groupadd -g 1000 app && \
    useradd -u 1000 -g 1000 -m app

WORKDIR /app

# copia venv
COPY --from=builder /app/.venv /app/.venv

# copia código
COPY app/ ./app/
COPY fonts/ ./fonts/

ENV PATH="/app/.venv/bin:$PATH"

# cria pastas (sem chown agressivo)
RUN mkdir -p /app/data /app/logs

# muda para usuário correto
USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
