FROM python:3.12-slim

# Set working directory
WORKDIR /workspace

# Copy workspace configuration
COPY pyproject.toml uv.lock ./

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Copy shared package first (dependency for app)
COPY shared/ shared/

# Copy app package
COPY app/ app/

# Install dependencies for app project
RUN uv sync --project app --no-dev

EXPOSE 8000

# Run the app
CMD ["uv", "run", "--project", "app", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]