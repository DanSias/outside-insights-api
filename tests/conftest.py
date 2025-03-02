import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base, get_db
from app.main import app  # Import FastAPI app

# Create a separate test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Test database fixture
@pytest.fixture(scope="function")
def db():
    """Create a new database session for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


# Override the dependency in FastAPI to use the test DB
app.dependency_overrides[get_db] = lambda: db


# Test client fixture
@pytest.fixture(scope="module")
def client():
    """Provides a test client for API requests."""
    with TestClient(app) as c:
        yield c
