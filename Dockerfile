# Stage 1: Build dependencies in isolated builder stage
FROM python:3.12-slim as builder

WORKDIR /install

# Install build essentials if required for C-extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /install/requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Minimal hardened runtime image
FROM python:3.12-slim

# Install curl for reliable healthcheck probes
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Security hardening: Create unprivileged application user
RUN groupadd -g 10001 acharya && \
    useradd -u 10001 -g acharya -m -s /bin/bash acharya

# Copy pre-built wheels and packages from builder stage
COPY --from=builder /install /usr/local

WORKDIR /app

# Ensure data directory exists and assign permissions to unprivileged user
RUN mkdir -p /app/app/data && chown -R acharya:acharya /app

# Copy application source code
COPY --chown=acharya:acharya . /app

# Switch execution to non-root user
USER acharya

# Runtime environment settings
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    PYTHONPATH=/app

EXPOSE 8000

# Continuous container liveness healthcheck against FastAPI /health probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Launch production server via Uvicorn ASGI
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
