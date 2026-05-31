import time
from datetime import timedelta


def test_register(client):
    """ Test user registration """
    response = client.post("/auth/register", json={"username": "testuser", "password": "testpass1"})
    assert response.status_code == 201
    assert response.json == {"message": "User registered successfully"}  # Fix assertion to match response


def test_register_weak_password(client):
    """ Test weak passwords are rejected by policy """
    response = client.post("/auth/register", json={"username": "weakuser", "password": "weakpass"})
    assert response.status_code == 400
    assert "number" in response.json["error"]


def test_login(client):
    """ Test user login """
    client.post("/auth/register", json={"username": "testuser", "password": "testpass1"})  # Register user first
    response = client.post("/auth/login", json={"username": "testuser", "password": "testpass1"})
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json

def test_invalid_login(client):
    """ Test login with non-existent user """
    response = client.post("/auth/login", json={"username": "nonexistent", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json == {"error": "Invalid credentials"}


def test_login_wrong_password(client):
    """ Test login fails when password is incorrect """
    client.post("/auth/register", json={"username": "testuser2", "password": "correctpass1"})
    response = client.post("/auth/login", json={"username": "testuser2", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json == {"error": "Invalid credentials"}


def test_login_seed_admin_password(client):
    """ Test seeded admin user requires correct password """
    bad_response = client.post("/auth/login", json={"username": "admin", "password": "ignored"})
    assert bad_response.status_code == 401

    good_response = client.post("/auth/login", json={"username": "admin", "password": "adminpass"})
    assert good_response.status_code == 200
    assert "access_token" in good_response.json


def test_refresh_issues_new_access_token(client):
    """ Test refresh token can issue a new access token """
    response = client.post("/auth/login", json={"username": "admin", "password": "adminpass"})
    assert response.status_code == 200

    refresh_token = response.json["refresh_token"]
    refresh_response = client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json


def test_access_token_expiry_and_refresh(client):
    """ Test access token expiration and obtaining a fresh token via refresh """
    client.application.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=1)
    client.application.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=5)

    login_response = client.post("/auth/login", json={"username": "admin", "password": "adminpass"})
    assert login_response.status_code == 200

    access_token = login_response.json["access_token"]
    refresh_token = login_response.json["refresh_token"]

    # Allow short-lived access token to expire
    time.sleep(2)

    expired_response = client.get(
        "/resources/tasks",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert expired_response.status_code == 401

    refresh_response = client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert refresh_response.status_code == 200
    new_access_token = refresh_response.json["access_token"]

    valid_response = client.get(
        "/resources/tasks",
        headers={"Authorization": f"Bearer {new_access_token}"}
    )
    assert valid_response.status_code == 200
