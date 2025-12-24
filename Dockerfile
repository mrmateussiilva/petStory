# Use official uv image for faster builds
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY app/ ./app/

# Copy fonts directory (directory exists in repo, so this should work)
# If fonts directory doesn't exist, create empty one first
RUN mkdir -p ./fonts
COPY fonts/ ./fonts/

# Make sure we use the venv
ENV PATH="/app/.venv/bin:$PATH"

# Create directories for temp and logs
RUN mkdir -p /app/temp /app/logs

# Expose port
EXPOSE 8000

# Health check (using urllib instead of requests to avoid extra dependency)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

