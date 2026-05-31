FROM python:3.12-slim

WORKDIR /app

# system basics (verhindert typische build errors)
RUN apt-get update && apt-get install -y \
    curl \
    iputils-ping \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# install uv
RUN pip install uv

# dependencies first (better caching)
COPY pyproject.toml uv.lock README.md ./

RUN uv sync --frozen --no-dev

# app code
COPY . .

RUN uv run python src/server/webapp/frontend/manage.py collectstatic --noinput

ENV PYTHONUNBUFFERED=1

EXPOSE 4040

# entry via your django project
CMD ["uv", "run", "server"]
