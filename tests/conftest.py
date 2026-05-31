import sys
import os

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Ensure deterministic seeded credentials for test runs
os.environ.setdefault("SEED_ADMIN_PASSWORD", "adminpass")
os.environ.setdefault("SEED_USER_PASSWORD", "johnpass")

import redis
import pytest
from app import create_app  # Now it should work!
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    """Creates and configures a new Flask app instance for each test"""
    app = create_app()
    app.config["TESTING"] = True  # Enables Flask test mode
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing
    return app

@pytest.fixture
def client(app):
    """Creates a test client using the Flask app fixture"""
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers(client):
    """Creates authentication headers for an admin user inside app context"""
    with client.application.app_context():  # Use app context from test client
        access_token = create_access_token(identity="admin")
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture(scope="function", autouse=True)
def clear_rate_limits():
    """Clears Redis rate limits before each test"""
    try:
        redis_client = redis.Redis(host="localhost", port=6379, db=0)
        redis_client.flushall()  # Reset rate limits
    except redis.exceptions.ConnectionError:
        print("⚠️ Redis is not running! Rate limit tests may fail.")
    yield
