# Usage Dashboard

A dashboard application for visualizing credit usage in the Orbital Copilot system.

## Project Structure

```
/
├── backend/              # FastAPI backend
│   ├── Dockerfile       # Backend Docker configuration
│   ├── .env            # Backend environment variables
│   ├── main.py         # Main API code
│   └── requirements.txt # Python dependencies
├── frontend/           # React frontend
│   ├── Dockerfile     # Frontend Docker configuration
│   ├── .env          # Frontend environment variables
│   ├── src/          # Source code
│   └── package.json  # Node.js dependencies
└── docker-compose.yml # Docker Compose configuration
```

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

### Development Mode

For development with hot-reload:

1. Create a docker-compose.override.yml:
```yaml
version: '3.8'

services:
  backend:
    volumes:
      - ./backend:/app
    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

  frontend:
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: ["npm", "start"]
```

2. Run with development configuration:
```bash
docker-compose -f docker-compose.yml -f docker-compose.override.yml up
```

### Environment Variables

Backend:
- `ENVIRONMENT`: development/production
- `ALLOWED_ORIGINS`: CORS allowed origins
- `LOG_LEVEL`: Logging level

Frontend:
- `REACT_APP_API_URL`: Backend API URL
- `NODE_ENV`: development/production

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

## Troubleshooting

### Common Issues

1. Port conflicts:
   - Change the port mapping in docker-compose.yml
   - Default ports: 3000 (frontend), 8000 (backend)

2. Container communication:
   - Check network configuration in docker-compose.yml
   - Verify service names in connection URLs

3. Performance issues:
   - Adjust container resource limits in docker-compose.yml
   - Monitor container metrics with `docker stats`

### Debug Mode

Run containers with debug logging:
```bash
docker-compose up --build -d && docker-compose logs -f
```

## Maintenance

### Updating Dependencies

1. Backend:
```bash
docker-compose run backend pip freeze > requirements.txt
```

2. Frontend:
```bash
docker-compose run frontend npm update
```

### Backup

Backup project data:
```bash
docker-compose down
tar -czf backup.tar.gz .
```

## Contributing

1. Create a feature branch
2. Make changes
3. Run tests:
```bash
docker-compose run backend pytest
docker-compose run frontend npm test
```
4. Submit pull request