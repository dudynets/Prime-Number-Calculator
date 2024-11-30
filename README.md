# Prime Number Calculator

A web application that calculates the Nth prime number using a distributed task system. Built with React, Flask, Dramatiq, PostgreSQL, and Redis.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:

```bash
git clone <repository-url>
cd <project-directory>
```

2. Build and start the containers:

```bash
docker-compose up --build
```

This will start the following services:

- Frontend (React) - http://localhost:80
- Backend (Flask) - http://localhost:4200
- PostgreSQL Database - localhost:5432
- Redis - localhost:6379
- Two worker nodes for processing prime number calculations

## Project Structure

The project consists of two main components:

1. Frontend (`/frontend`):

   - React application with TypeScript
   - Material-UI for styling
   - JWT authentication

2. Backend (`/backend`):
   - Flask REST API
   - PostgreSQL database
   - Redis for task queue
   - Dramatiq for distributed task processing

## Features

- User registration and authentication
- Calculate Nth prime number with progress tracking
- Cancel running calculations
- View calculation history
- Delete completed calculations

## API Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create new calculation task
- `GET /api/tasks/:id` - Get task details
- `POST /api/tasks/:id/cancel` - Cancel running task
- `DELETE /api/tasks/:id` - Delete completed task

## Development

To make changes to the code and see them reflected:

```bash
docker-compose down
docker-compose up --build
```

## Cleanup

To stop and remove all containers:

```bash
docker-compose down -v
```

The `-v` flag also removes the persistent volume used by PostgreSQL.

## License

Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License.
See [LICENSE](LICENSE) for more information.
