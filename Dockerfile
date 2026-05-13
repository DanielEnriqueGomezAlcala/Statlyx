FROM python:3.13

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev

COPY src/ ./src/
COPY templates/ ./templates/

EXPOSE 8050

CMD ["uv", "run", "python", "src/dashboard.py"]
