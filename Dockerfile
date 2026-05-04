FROM python:3.14-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build


RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

#  Stage 2: production image
FROM python:3.14-slim AS production

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        libexpat1 \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN groupadd -r diary && useradd -r -g diary diary

WORKDIR /app

# Copy compiled venv from builder
COPY --from=builder /venv /venv

# Copy project (honours .dockerignore)
COPY --chown=diary:diary . .

# Ensure the logs directory exists and is writable by the runtime user
RUN mkdir -p /app/logs && chown diary:diary /app/logs


USER diary

# uWSGI serves on TCP 0.0.0.0:8000; override CMD for management commands
CMD ["uwsgi", "--enable-threads", "--ini", "diary.ini"]
