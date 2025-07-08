FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD ./app /app

WORKDIR /app

RUN uv sync --locked --no-dev

EXPOSE 8000

CMD ["uv", "run", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]