# Usage Dashboard

A dashboard application for visualizing credit usage in the Orbital Copilot system.

## Running with Docker

### Prerequisites

- Docker
- Docker Compose

### Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd usage-dashboard
```

2. Start the services:
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Individual Container Management

Start specific services:
```bash
docker-compose up backend  # Start only the backend
docker-compose up frontend # Start only the frontend
```

View logs:
```bash
docker-compose logs -f    # All services
docker-compose logs -f backend  # Backend only
docker-compose logs -f frontend # Frontend only
```

Stop services:
```bash
docker-compose down       # Stop all services
docker-compose down -v    # Stop all services and remove volumes
```


## Testing

Run tests inside Docker:

```bash
# Backend tests
docker-compose run backend pytest

# Frontend tests
docker-compose run frontend npm test
```

## Production Deployment

For production deployment:

1. Update environment variables:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

2. Edit the .env files with production values

3. Build and run:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```


