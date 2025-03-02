# Outside Insights API Backend

A FastAPI-based backend for proxying requests to various LLM providers and logging responses.

## Features

- 🔐 Authentication and authorization with JWT
- 👥 Organizations and teams management
- 🤖 Multiple LLM providers integration (OpenAI, Anthropic, Cohere)
- 📊 Response logging and analytics
- 🔄 Asynchronous request handling
- 📝 Comprehensive API documentation with Swagger UI
- 🐳 Docker support for easy deployment

## Project Structure

The project follows a clean architecture with separation of concerns:

- **API**: FastAPI routes and endpoints
- **Models**: SQLAlchemy database models
- **Schemas**: Pydantic validation schemas
- **Services**: Business logic and LLM integrations
- **Core**: Core functionality like authentication and configuration
- **DB**: Database connection and CRUD operations
- **Tests**: Unit and integration tests

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ai-api-backend.git
   cd ai-api-backend
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -e .
   ```

4. Create a `.env` file based on `.env.example`:

   ```bash
   cp .env.example .env
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Setup

1. Build and run with Docker Compose:

   ```bash
   docker-compose up -d
   ```

2. Access the API at http://localhost:8000

## API Documentation

Once the application is running, you can access the Swagger UI at:

- http://localhost:8000/docs
- http://localhost:8000/redoc

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

```bash
alembic revision --autogenerate -m "Add new field"
alembic upgrade head
```

## Usage Examples

### Authentication

```python
import requests

# Login to get access token
response = requests.post(
    "http://localhost:8000/api/v1/auth/token",
    data={"username": "user@example.com", "password": "password"}
)
token = response.json()["access_token"]

# Use the token for authenticated requests
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/api/v1/users/me", headers=headers)
```

### Sending a Prompt

```python
import requests

# Send a prompt to OpenAI
response = requests.post(
    "http://localhost:8000/api/v1/prompts/",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "content": "Explain quantum computing in simple terms",
        "llm_provider": "openai",
        "parameters": {
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 500
        }
    }
)

# Get the response
result = response.json()
print(result["response_content"])
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
