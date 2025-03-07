FROM python:3.11-slim

WORKDIR /app/

# Install Poetry
RUN pip install poetry==1.8.2

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Configure poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY . /app/

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos "" app
USER app

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]