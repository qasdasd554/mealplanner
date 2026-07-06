"""Shared pytest fixtures for Smart Meal Planner PL backend tests."""
import os
import uuid
import pytest
import requests
from dotenv import load_dotenv

load_dotenv("/app/frontend/.env")

BASE_URL = os.environ["EXPO_PUBLIC_BACKEND_URL"].rstrip("/")
API = f"{BASE_URL}/api"

TEST_EMAIL = "test@mealplanner.pl"
TEST_PASSWORD = "Test123!"


@pytest.fixture(scope="session")
def api_base():
    return API


@pytest.fixture(scope="session")
def http():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="session")
def auth_token(http):
    # Login with pre-existing test user, fallback to register
    r = http.post(f"{API}/auth/login", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    if r.status_code == 200:
        return r.json()["token"]
    r = http.post(f"{API}/auth/register", json={
        "email": TEST_EMAIL, "password": TEST_PASSWORD, "display_name": "Test User"
    })
    assert r.status_code == 201, f"Register failed: {r.status_code} {r.text}"
    return r.json()["token"]


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}


@pytest.fixture(scope="session")
def fresh_user(http):
    """Create a brand new user for isolated tests."""
    email = f"TEST_{uuid.uuid4().hex[:8]}@mealplanner.pl"
    r = http.post(f"{API}/auth/register", json={
        "email": email, "password": "Test123!", "display_name": "Fresh Tester"
    })
    assert r.status_code == 201, r.text
    data = r.json()
    return {
        "email": email,
        "token": data["token"],
        "user": data["user"],
        "headers": {"Authorization": f"Bearer {data['token']}", "Content-Type": "application/json"},
    }
