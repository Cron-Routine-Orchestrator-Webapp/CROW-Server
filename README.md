<p align="center">
  <img src="https://github.com/Cron-Routine-Orchestrator-Webapp/.github/blob/main/assets/icon.png?raw=true" alt="Logo" width=200px />
</p>

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Cron-Routine-Orchestrator-Webapp/CROW-Server)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/Cron-Routine-Orchestrator-Webapp/CROW-Server?style=flat&link=https%3A%2F%2Fgithub.com%2FCron-Routine-Orchestrator-Webapp%2FCROW-Server%2Fissues)](https://github.com/Cron-Routine-Orchestrator-Webapp/CROW-Server/issues)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-pr/Cron-Routine-Orchestrator-Webapp/CROW-Server?style=flat&color=%230000ff&link=https%3A%2F%2Fgithub.com%2FCron-Routine-Orchestrator-Webapp%2FCROW-Server%2Fpulls)](https://github.com/Cron-Routine-Orchestrator-Webapp/CROW-Server/pulls)
[![GitHub License](https://img.shields.io/github/license/Cron-Routine-Orchestrator-Webapp/CROW-Server?style=flat&color=%237f3403)](https://github.com/Cron-Routine-Orchestrator-Webapp/CROW-Server?tab=Apache-2.0-1-ov-file#readme)
[![GitHub Release](https://img.shields.io/github/v/release/Cron-Routine-Orchestrator-Webapp/CROW-Server?display_name=tag&style=flat&label=GitHub%20Release&color=%233e85e0)](https://github.com/Cron-Routine-Orchestrator-Webapp/CROW-Server/releases/latest)

# CROW-Server

**CROW** (Cron Routine Orchestrator Webapp) is a comprehensive web-based application for managing and scheduling cron jobs. This repository contains the backend server component responsible for managing all cron jobs, maintaining the web interface, handling real-time communication with clients, and providing a REST API for job orchestration.

## Overview

CROW-Server is built with Python using Django and Django Channels, providing:

- A full-featured web dashboard for job management
- WebSocket-based real-time communication with remote clients
- A robust backend system for cron job scheduling and execution
- Database persistence for jobs, tasks, and client information

## Features

- 🎯 **Intuitive Web Dashboard** - Manage and monitor all your cron jobs from a centralized web interface
- ⚡ **Real-time Updates** - WebSocket communication for live job status updates
- 🔄 **Client Management** - Connect and manage multiple remote CROW clients
- 📅 **Job Scheduling** - Create and manage cron-based job schedules with flexible recurring options
- 🗂️ **Task Organization** - Organize jobs into logical tasks for better management
- 📊 **Monitoring & Logging** - Track job execution history and performance metrics
- 🔌 **API-First Design** - RESTful API endpoints for programmatic job management
- 📱 **Responsive Design** - Works seamlessly across desktop and mobile devices

# Docker Installation

CROW Server is distributed as a Docker image via GitHub Container Registry (GHCR).

The image is available at:

```text
ghcr.io/cron-routine-orchestrator-webapp/crow-server:latest
```

## Requirements

### Linux

- Docker Engine
- Docker Compose (recommended)

### Windows

- Docker Desktop

### macOS

- Docker Desktop

Verify your installation:

```bash
docker --version
docker compose version
```

---

## Installation with Docker

Create a directory for persistent application data, the application will live there:

```bash
mkdir crow_sever
```

Start the container, by running this in the directory:

```bash
docker run -d \
  --name crow-server \
  -p 4040:4040 \
  -e USE_DOCKER=1 \
  -e DEBUG=0 \
  -e DB_PATH=/data/db.sqlite3 \
  -v $(pwd)/data:/data \
  ghcr.io/cron-routine-orchestrator-webapp/crow-server:latest
```

The web interface will be available at:

```text
http://localhost:4040
```

### View Logs

```bash
docker logs -f crow-server
```

### Stop the Container

```bash
docker stop crow-server
```

### Remove the Container

```bash
docker rm -f crow-server
```

---

## Updating a Docker Installation

Pull the latest image:

```bash
docker pull ghcr.io/cron-routine-orchestrator-webapp/crow-server:latest
```

Recreate the container:

```bash
docker rm -f crow-server

docker run -d \
  --name crow-server \
  -p 4040:4040 \
  -e USE_DOCKER=1 \
  -e DEBUG=0 \
  -e DB_PATH=/data/db.sqlite3 \
  -v $(pwd)/data:/data \
  ghcr.io/cron-routine-orchestrator-webapp/crow-server:latest
```

All application data remains intact because it is stored in the mounted `data` directory.

---

## Installation with Docker Compose (Recomended)

Create a `docker-compose.yml` file:

```yaml
version: "3.9"

services:
  crow-server:
    image: ghcr.io/cron-routine-orchestrator-webapp/crow-server:latest

    container_name: crow-server

    restart: unless-stopped

    ports:
      - "4040:4040"

    environment:
      USE_DOCKER: "1"
      DB_PATH: /data/db.sqlite3
      SECRET_KEY: "django-insecure-8orjtc^_c$t03$m(8sry8(6#xny77ad^-%ur16gygdw!j#6=c("
      DEBUG: "0"
      ALLOWED_HOSTS: "*"

    volumes:
      - ./data:/data
```

Create the application directory:

```bash
mkdir crow-server
```

Start the application:

```bash
docker compose up -d
```

The web interface will be available at:

```text
http://localhost:4040
```

### View Logs

```bash
docker compose logs -f
```

### Stop the Application

```bash
docker compose down
```

---

## Updating a Docker Compose Installation

Pull the newest image:

```bash
docker compose pull
```

Recreate the container:

```bash
docker compose up -d
```

Verify the running version:

```bash
docker ps
```

All application data remains intact because it is stored in the mounted `data` directory.

---

# Data Persistence

CROW Server stores its SQLite database in:

```text
./data/db.sqlite3
```

This location is mapped to the host system through a Docker volume. Updating or recreating containers will not remove your data as long as the `data` directory is preserved.

### Project Structure

```
src/server/
├── __init__.py
├── __main__.py              # Entry point for the server
├── base.html                # Base HTML template
└── webapp/
    ├── backend/             # Backend logic and cron scheduling
    │   ├── cron_backend/    # Cron job scheduling engine
    │   ├── helper/          # Utility functions and type definitions
    │   └── websocket_communication/  # WebSocket handlers for real-time communication
    └── frontend/            # Django web interface
        ├── database_backend.py       # Database configuration
        ├── manage.py         # Django management script
        ├── frontend/         # Main Django app configuration
        ├── ui/               # User interface application
        │   ├── models.py     # Database models (Jobs, Tasks, Clients)
        │   ├── views.py      # View controllers
        │   ├── urls.py       # URL routing
        │   ├── admin.py      # Django admin configuration
        │   ├── static/       # CSS and static files
        │   └── templates/    # HTML templates
        └── db.sqlite3        # SQLite database
```

## Architecture

CROW-Server consists of three main components:

1. **Frontend (Django Web Interface)**
   - RESTful API endpoints
   - HTML/CSS web dashboard
   - Job and task management interfaces

2. **Backend (Cron Engine)**
   - Cron job scheduling and execution
   - Job state management
   - Task queuing and processing
   - Cron clock for time-based operations

3. **WebSocket Communication Layer**
   - Real-time client-server messaging
   - Job status updates
   - Command execution on remote clients
   - Bidirectional communication handler

## API Documentation

The server provides a RESTful API for managing:

- **Jobs** - Create, read, update, delete jobs
- **Tasks** - Organize and manage task definitions
- **Clients** - Register and manage connected clients

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for information on how to get started.

Key areas for contribution:

- Bug fixes and improvements
- Documentation enhancements
- Feature implementations
- Performance optimizations
- Test coverage improvements

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming and inclusive community.

## Related Projects

- **[CROW-Client](https://github.com/Cron-Routine-Orchestrator-Webapp/CROW-Client)** - Remote client for executing scheduled jobs
- **[CROW Organization](https://github.com/Cron-Routine-Orchestrator-Webapp)** - Main organization repository

## Documentation

For comprehensive documentation, visit:

- **[Documentation (DeepWiki)](https://deepwiki.com/Cron-Routine-Orchestrator-Webapp/CROW-Server)**
- **[CROW-Client Documentation](https://deepwiki.com/Cron-Routine-Orchestrator-Webapp/CROW-Client)**

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 Report issues on [GitHub Issues](https://github.com/Cron-Routine-Orchestrator-Webapp/CROW-Server/issues)
- 💬 Join discussions and ask questions
- 📚 Check the [documentation](https://deepwiki.com/Cron-Routine-Orchestrator-Webapp/CROW-Server)
- 🐛 Help us improve by providing feedback
