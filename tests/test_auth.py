def test_register(client):
    """ Test user registration """
    response = client.post("/auth/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201
    assert response.json == {"message": "User registered successfully"}  # Fix assertion to match response

def test_login(client):
    """ Test user login """
    client.post("/auth/register", json={"username": "testuser", "password": "testpass"})  # Register user first
    response = client.post("/auth/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json

def test_invalid_login(client):
    """ Test login with non-existent user """
    response = client.post("/auth/login", json={"username": "nonexistent", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json == {"error": "Invalid credentials"}


def test_login_wrong_password(client):
    """ Test login fails when password is incorrect """
    client.post("/auth/register", json={"username": "testuser2", "password": "correctpass"})
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
