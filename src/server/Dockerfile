FROM python:3.12-slim

WORKDIR /app

# system basics (verhindert typische build errors)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# install uv
RUN pip install uv

# dependencies first (better caching)
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

# app code
COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# entry via your django project
CMD ["uv", "run", "server"]