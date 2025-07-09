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
COPY broker/ broker/

# Install dependencies for app project
RUN uv sync --project broker --no-dev

# Run the app
CMD ["python", "-c", "print('Write custom startup logic in compose')"]