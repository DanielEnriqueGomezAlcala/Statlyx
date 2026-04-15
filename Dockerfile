FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev

COPY src/ ./src/
COPY templates/ ./templates/

EXPOSE 8050

CMD ["uv", "run", "python", "src/dashboard.py"]
