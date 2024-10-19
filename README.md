
# FastAPI Performance Comparison: Synchronous vs Asynchronous

This project aims to study the performance differences between synchronous and asynchronous FastAPI endpoints using **Python 3.12** and the **alpine** Docker image. The project is set up with Docker Compose, with a PostgreSQL database and performance tests using **Apache Benchmark (ab)**.

## Table of Contents
- [Project Setup](#project-setup)
- [Running the Application](#running-the-application)
- [Testing Performance](#testing-performance)
  - [Command Overview](#command-overview)
  - [Asynchronous Test Results](#asynchronous-test-results)
  - [Synchronous Test Results](#synchronous-test-results)
  - [Comparison Table](#comparison-table)
- [Development Environment](#development-environment)
- [Unit Tests](#unit-tests)
- [Future Improvements](#future-improvements)

## Project Setup

The project uses the following components:
- **FastAPI**: Web framework for building the API.
- **PostgreSQL**: Database used for storing notes.
- **Docker & Docker Compose**: For containerizing and managing the development environment.
- **Apache Benchmark (ab apache2-utils)**: To measure performance between synchronous and asynchronous endpoints.

### Docker Compose Configuration

Here’s the `docker-compose.yml` configuration used in this project:

```yaml
version: '3'

services:
  web:
    build: .
    volumes:
      - ./:/usr/src/app/
    ports:
      - 8000:8000
    environment:
      - DATABASE_URL=postgresql://admin:admin@db/fastapi_dev
    depends_on:
      - db
    tty: true

  db:
    image: postgres:15.1-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    expose:
      - 5432
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}

volumes:
  postgres_data:
```

### PostgreSQL Environment Variables

Ensure you have the following variables defined in your `.env` file:
```bash
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=fastapi_dev
```

### Building the Image

Before running the application, build the Docker image using:
```bash
docker-compose build
```

## Running the Application

To start the application and all services (FastAPI and PostgreSQL), run:

```bash
docker-compose up
```

This will start FastAPI on `http://localhost:8000` and PostgreSQL in the background.

You can access the FastAPI documentation at `http://localhost:8000/docs`.

## Testing Performance

We compare two endpoints:
- **Asynchronous**: `/notes/` (Handles requests asynchronously)
- **Synchronous**: `/notes/sync/` (Handles requests synchronously)

### Command Overview

We use **Apache Benchmark (ab)** to run the performance tests. The following commands are used for testing the endpoints:

- **Async Endpoint Test**:
  ```bash
  ab -v 2 -p ./data/note.json -T application/json -n 10000 -c 10 http://localhost:8000/notes/
  ```

- **Sync Endpoint Test**:
  ```bash
  ab -v 2 -p ./data/note.json -T application/json -n 10000 -c 10 http://localhost:8000/notes/sync/
  ```

### Asynchronous Test Results

**Command**:
```bash
ab -v 2 -p ./data/note.json -T application/json -n 10000 -c 10 http://localhost:8000/notes/
```

**Results**:
- **Requests per second**: ~476.25
- **Average time per request**: 21 ms
- **Max time**: 585 ms
- **Total data transfer**: 48.59 Kbytes/sec

**Detailed Breakdown**:

| Percentile | Response Time (ms) |
|------------|--------------------|
| 50%        | 21                 |
| 75%        | 23                 |
| 90%        | 25                 |
| 95%        | 27                 |
| 99%        | 30                 |
| 100%       | 585 (longest)      |

### Synchronous Test Results

**Command**:
```bash
ab -v 2 -p ./data/note.json -T application/json -n 10000 -c 10 http://localhost:8000/notes/sync/
```

**Results**:
- **Requests per second**: ~124.70
- **Average time per request**: 80.19 ms
- **Max time**: 300 ms
- **Total data transfer**: 48.59 Kbytes/sec

**Detailed Breakdown**:

| Percentile | Response Time (ms) |
|------------|--------------------|
| 50%        | 77                 |
| 75%        | 99                 |
| 90%        | 129                |
| 95%        | 164                |
| 99%        | 203                |
| 100%       | 300 (longest)      |

### Comparison Table

| Metric                         | Async                         | Sync                           |
|--------------------------------|-------------------------------|--------------------------------|
| **Requests per second**        | 476.25                        | 124.70                         |
| **Average time per request**   | 21 ms                         | 80.19 ms                       |
| **Max response time**          | 585 ms                        | 300 ms                         |
| **Median response time**       | 21 ms                         | 77 ms                          |
| **Total data transfer**        | 48.59 Kbytes/sec              | 48.59 Kbytes/sec               |

### Insights:

- **Asynchronous Endpoint**:
  - Handles significantly more requests per second (~476) compared to the synchronous one (~124).
  - The response times are lower and more consistent, making the async approach more performant under high load.
  
- **Synchronous Endpoint**:
  - Although simpler, it has higher latencies, especially when dealing with concurrent requests. The average time per request is around 4 times slower than the async implementation.

## Development Environment

To facilitate development, the project is set up with a **DevContainer** using VS Code. This ensures a consistent development environment with pre-installed dependencies and tools.

### DevContainer Configuration

```json
{
	"name": "App",
	"dockerComposeFile": [
		"../docker-compose.yml"
	],
	"service": "web",
	"workspaceFolder": "/workspaces/${localWorkspaceFolderBasename}",
	"customizations": {
		"vscode": {
			"extensions": [
				"ckolkman.vscode-postgres"
			]
		}
	}
}
```

## Unit Tests

Unit tests are provided to ensure the functionality of the API. Run the tests inside the container using:

```bash
pytest .
```

## Future Improvements

- Add support for load testing other endpoints.
- Investigate scaling FastAPI with multiple workers for performance improvements.
- Automate performance benchmarks and reporting for better insight.
