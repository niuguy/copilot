
### Prerequisites

- Docker and Docker Compose (for containerized setup)
- Python 3.11 (Do not use 3.12 as aiohttp is not compatible with it yet)
- Node.js 14+ (for non-Docker frontend setup)

### Installation and Running the Application

#### Using Docker Compose (Recommended)

Build and start the containers:
   ```
   docker-compose up --build
   ```

   This will start both the backend and frontend services.

#### Without Docker Compose

If you prefer to run the services directly on your machine:

1.Set up and run the backend:

   ```
   cd backend
   python -m venv venv (recommend using uv which is faster)
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   python app.py  # Or the appropriate command to start your backend server
   ```

2.In a new terminal, set up and run the frontend:
   ```
   cd frontend
   npm install
   npm run dev
   ```

## Running the tests

To run the tests directly on your machine:

1. Ensure you're in the backend directory and your virtual environment is activated.

2. Run the tests:
   ```
   pytest
   ```

   To run specific test files or directories:
   ```
   pytest path/to/test_file.py
   ```

   To run tests with additional pytest options:
   ```
   pytest -v -s
   ```

## Key Decisions
- I used aiohttp to make API calls asynchronously to improve the performance.Compared to multithreading, async is light weight and does not require the GIL.
- I put everything in one api endpoint to avoid making too many api calls.
- I put the bar chart data in the backend to avoid calculating the data on the frontend and make it easier to cache the data in the backend.
- I added docker compose to make it easier to deploy to different environments later.

## Potential Improvements

- Add end to end tests using frameworks like Playwright or Selenium.
- Add caching mechanism in the backend using services like Redis.
- Backend could be more modularized and set up service layer if there are more API endpoints.
- Better styling and layout using some UI libraries.
- Monitoring the api request rates and make sure it does not get rate limited.
