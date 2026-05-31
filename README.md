# API in a Flask

A personal project demonstrating how to build a secure REST API using Flask, Python, and industry-standard security practices. This API provides user authentication with JWT tokens, resource management, rate limiting, and comprehensive test coverage.

**Status:** Active development | **Python Version:** 3.8+ | **Flask Version:** 3.1.0

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Authorization and Roles](#authorization-and-roles)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Rate Limiting](#rate-limiting)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Helper Scripts](#helper-scripts)
- [Future Improvements](#future-improvements)

## Overview

API in a Flask is a demonstration REST API built with Flask that showcases secure authentication patterns, password hashing, JWT token management, and resource-based access control. The project is suitable for learning Flask API development, security best practices, and testing strategies.

The API manages resources (tasks, etc.) with full CRUD operations, enforced authentication, role-based authorization (admin vs. user), and rate limiting to prevent abuse.

## Features

- **Secure User Authentication**
  - User registration with password policy enforcement
  - Login with JWT access and refresh tokens
  - Password storage using Werkzeug salted hashing (PBKDF2-SHA256)
  - Token expiration and refresh mechanism

- **Resource Management**
  - Full CRUD operations on generic resource types
  - Resource-type-based storage (tasks, etc.)
  - Automatic ID assignment

- **Authorization & Access Control**
  - Role-based access control (admin, user)
  - Protected endpoints requiring JWT
  - Admin-only operations for create/update/delete

- **Security Features**
  - Input validation and sanitization (regex-based)
  - CORS support with configurable origins
  - Rate limiting on sensitive endpoints (3 per minute for updates)
  - Secure subprocess execution
  - Secure temporary file handling

- **Rate Limiting**
  - Redis-backed rate limiting
  - Configurable moving-window strategy
  - Custom 429 error responses

- **Testing**
  - Comprehensive pytest suite
  - Auth testing (registration, login, password hashing)
  - Token expiry and refresh token tests
  - Rate limit verification
  - Resource CRUD tests
  - Test fixtures with auth headers

## Technology Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Flask | 3.1.0 | Web framework |
| Python | 3.8+ | Language |
| Werkzeug | 3.1.3 | Security utilities (password hashing) |
| Flask-JWT-Extended | 4.7.1 | JWT token generation and validation |
| Flask-Limiter | 3.10.1 | Rate limiting |
| Redis | Latest | Rate limiter storage backend |
| Flask-CORS | 5.0.0 | Cross-origin resource sharing |
| pytest | 8.3.4 | Testing framework |
| python-dotenv | 1.0.1 | Environment variable management |

## Project Structure

```
API-in-a-Flask/
├── app/                          # Main application package
│   ├── __init__.py              # App factory (create_app)
│   ├── auth.py                  # Authentication routes (register, login, refresh)
│   ├── routes.py                # Resource management routes (CRUD)
│   ├── models.py                # In-memory data store and seeded users
│   └── config.py                # Configuration and Flask limiter setup
├── utils/
│   └── security_utils.py        # Security helpers (hashing, input validation)
├── tests/
│   ├── conftest.py              # pytest fixtures and Redis setup
│   ├── test_auth.py             # Authentication tests
│   └── test_routes.py           # Resource CRUD and rate limit tests
├── run.py                        # Application entry point
├── setup.sh                      # Automated setup script (Linux/Fedora)
├── set_env.sh                    # JWT token fetcher helper
├── requirements.txt             # Python dependencies
├── .env                          # Environment variables (git-ignored)
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Quick Start

For the impatient, use the automated setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This handles: system updates, Redis installation, Python venv creation, dependency installation, .env bootstrapping, and test execution.

If you prefer manual setup, see [Setup Instructions](#setup-instructions) below.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Redis server (for rate limiting)
- Linux/Fedora/Ubuntu (or adapt package manager commands for your OS)
- curl and jq (optional, for set_env.sh helper)

### Manual Setup

1. Install system dependencies:

   **On Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-venv redis-server
   ```

   **On Fedora:**
   ```bash
   sudo dnf install -y python3-pip redis
   ```

2. Create and activate virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Upgrade pip:

   ```bash
   pip install --upgrade pip
   ```

4. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:

   ```bash
   cp .env.example .env  # if available, or create manually
   ```

   Or use the built-in bootstrap to create `.env`:

   ```bash
   cat > .env << 'EOF'
   SEED_ADMIN_PASSWORD=adminpass
   SEED_USER_PASSWORD=johnpass
   DEBUG=False
   CORS_ORIGINS=*
   EOF
   ```

6. Start Redis:

   **Using systemctl (Fedora):**
   ```bash
   sudo systemctl enable --now redis
   ```

   **Or directly:**
   ```bash
   redis-server --daemonize yes
   ```

7. Verify Redis is running:

   ```bash
   redis-cli ping
   # Expected output: PONG
   ```

## Running the Application

### Development Server

Activate your venv and run:

```bash
python run.py
```

The API will start on `http://127.0.0.1:8080`.

Expected output:
```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://10.x.x.x:8080
```

### Health Check

```bash
curl http://127.0.0.1:8080/
# Expected response:
# {"message": "Welcome to API in a Flask!"}, 200
```

## API Endpoints

### Authentication Endpoints

#### POST /auth/register

Register a new user account.

**Request:**
```json
{
  "username": "newuser",
  "password": "SecurePass123"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully"
}
```

**Response (400 - Validation Error):**
```json
{
  "error": "Password must be at least 8 characters long"
}
```

**Response (409 - Duplicate User):**
```json
{
  "error": "User already exists"
}
```

**Password Policy:**
- Minimum 8 characters
- At least one letter
- At least one number
- No spaces

#### POST /auth/login

Authenticate and receive JWT tokens.

**Request:**
```json
{
  "username": "admin",
  "password": "adminpass"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ0**********iLCJhbGc...",
  "refresh_token": "eyJ0**********iLCJhbGc..."
}
```

**Response (401):**
```json
{
  "error": "Invalid credentials"
}
```

#### POST /auth/refresh

Obtain a new access token using a refresh token.

**Request Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response (200):**
```json
{
  "access_token": "eyJ0**********iLCJhbGc..."
}
```

**Response (401):**
```json
{
  "error": "Invalid or expired token"
}
```

### Resource Endpoints

All resource endpoints require JWT authentication.

#### GET /resources/<resource_type>

Retrieve all resources of a given type (e.g., tasks).

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Example:**
```bash
curl -H "Authorization: Bearer <token>" http://127.0.0.1:8080/resources/tasks
```

**Response (200):**
```json
[
  {"id": 1, "name": "Complete project", "status": "In Progress"},
  {"id": 2, "name": "Write documentation", "status": "Pending"}
]
```

#### POST /resources/<resource_type>

Create a new resource (admin only).

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "New Task",
  "status": "Pending"
}
```

**Response (201):**
```json
{
  "id": 3,
  "name": "New Task",
  "status": "Pending"
}
```

**Response (403):**
```json
{
  "error": "Unauthorized"
}
```

#### PUT /resources/<resource_type>/<id>

Update an existing resource (admin only, rate-limited to 3 per minute).

**Request Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Updated Task",
  "status": "Completed"
}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "Updated Task",
  "status": "Completed"
}
```

**Response (429 - Rate Limited):**
```json
{
  "error": "Rate limit exceeded",
  "message": "3 per 1 minute"
}
```

#### DELETE /resources/<resource_type>/<id>

Delete a resource (admin only).

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "Item with ID 1 deleted from 'tasks'"
}
```

**Response (404):**
```json
{
  "error": "Item with ID 999 not found in 'tasks'"
}
```

## Authentication

### JWT Token Flow

1. **User Registration:** `/auth/register` - Creates a new user with hashed password.
2. **User Login:** `/auth/login` - Returns both `access_token` (short-lived) and `refresh_token` (long-lived).
3. **API Requests:** Include `Authorization: Bearer <access_token>` header.
4. **Token Refresh:** `/auth/refresh` - Use refresh token to obtain a new access token.
5. **Token Expiry:** Access tokens expire after a configured duration; refresh to continue.

### Password Security

- Passwords are hashed using Werkzeug's `generate_password_hash` with PBKDF2-SHA256 and random salt.
- Passwords are never stored in plaintext.
- Login validation uses `check_password_hash` to safely compare hashes.
- Seeded users (admin, john_doe) are created from environment variables `SEED_ADMIN_PASSWORD` and `SEED_USER_PASSWORD`.

### Token Storage

- Access tokens should be stored in memory or session storage (not localStorage in web apps without mitigation).
- Refresh tokens should be stored securely (httpOnly cookies in web apps).
- Never commit tokens or `.env` to version control.

## Authorization and Roles

### User Roles

- **admin:** Can create, read, update, and delete resources.
- **user:** Can only read resources (GET endpoints).

### Role Enforcement

The API checks the user's role before permitting mutating operations:
- `POST /resources/<type>` - admin only
- `PUT /resources/<type>/<id>` - admin only
- `DELETE /resources/<type>/<id>` - admin only
- `GET /resources/<type>` - authenticated users (any role)

## Environment Variables

Create a `.env` file in the project root (or set these in your shell):

| Variable | Default | Purpose |
|----------|---------|---------|
| `SEED_ADMIN_PASSWORD` | (required) | Admin account seeded password |
| `SEED_USER_PASSWORD` | (required) | john_doe user seeded password |
| `SECRET_KEY` | (random) | Flask session secret key |
| `JWT_SECRET_KEY` | (random) | JWT signing key |
| `DEBUG` | False | Enable Flask debug mode (never in production) |
| `CORS_ORIGINS` | * | Allowed CORS origins |

Example `.env`:
```
SEED_ADMIN_PASSWORD=adminpass
SEED_USER_PASSWORD=johnpass
DEBUG=False
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Testing

### Run All Tests

Ensure Redis is running, then:

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_auth.py -v
pytest tests/test_routes.py -v
```

### Run Specific Test

```bash
pytest tests/test_auth.py::test_login -v
```

### Test Coverage

Current test suite covers:

- User registration with password policy
- User login and JWT token generation
- Invalid login attempts
- Wrong password rejection
- Seeded user authentication
- Token refresh and expiry
- Resource CRUD operations
- Rate limit enforcement (3 updates per minute)
- Authorization checks (admin-only endpoints)

### Fixtures

Provided pytest fixtures (in `conftest.py`):
- `app` - Flask test app instance
- `client` - Flask test client
- `auth_headers` - Pre-generated admin JWT headers
- `clear_rate_limits` - Auto-clears Redis before each test

## Rate Limiting

### Configuration

Rate limiting is configured in `app/config.py`:
- **Backend:** Redis at `redis://localhost:6379`
- **Strategy:** Moving-window
- **Update Limit:** 3 requests per 60 seconds on PUT endpoints

### Limits Applied

- `PUT /resources/<type>/<id>` - 3 per minute (rate-limited)
- Other endpoints - no explicit limits (but Redis-backed, can be added)

### Rate Limit Response

When limit is exceeded (HTTP 429):
```json
{
  "error": "Rate limit exceeded",
  "message": "3 per 1 minute"
}
```

### Resetting Rate Limits

To reset rate limits during testing or development:
```bash
redis-cli FLUSHDB
```

Or from Python:
```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.flushall()
```

## Security Considerations

### What This API Does Well

- Passwords are hashed with PBKDF2-SHA256 and random salt (Werkzeug).
- Input validation with regex to prevent shell injection.
- JWT tokens for stateless authentication.
- Role-based access control.
- CORS headers to prevent unauthorized cross-origin requests.
- Rate limiting to prevent brute-force attacks.
- Environment-based secrets (not hardcoded).

### Limitations & What to Add for Production

1. **Database:** This API uses in-memory storage. Data is lost on process restart. Use a persistent database (PostgreSQL, MongoDB) for production.

2. **Password Reset:** No password reset flow. Add email-based reset tokens in production.

3. **Audit Logging:** No request logging or audit trail. Implement for compliance.

4. **HTTPS Only:** Always use HTTPS in production. This API runs over HTTP for local development.

5. **Token Blacklist:** No mechanism to revoke tokens. Use a blacklist (Redis) for logout functionality.

6. **CSRF Protection:** CSRF is disabled for testing (`WTF_CSRF_ENABLED`). Enable in production.

7. **Secrets Management:** Use environment variables, but consider Vault or AWS Secrets Manager for production.

8. **Input Validation:** Current regex is restrictive. Use libraries like `marshmallow` or Pydantic for robust validation.

9. **Rate Limiting:** Current limits are hardcoded. Make them dynamic per endpoint and per user.

10. **Error Messages:** Some error messages leak information (e.g., "User already exists" during registration). Use generic messages in production.

## Troubleshooting

### Redis Connection Error

**Error:**
```
redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379. Connection refused.
```

**Solution:**
1. Check Redis is running:
   ```bash
   redis-cli ping
   ```
2. Start Redis if not running:
   ```bash
   redis-server --daemonize yes
   ```
3. Or check Redis is installed:
   ```bash
   which redis-server
   ```

### ModuleNotFoundError: No module named 'app'

**Error:**
```
ModuleNotFoundError: No module named 'app'
```

**Solution:**
1. Ensure you are in the project root directory:
   ```bash
   pwd  # Should show /path/to/API-in-a-Flask
   ```
2. Ensure venv is activated:
   ```bash
   source venv/bin/activate
   ```
3. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### JWT Token Expired

**Error:**
```
{
  "error": "Token has expired"
}
```

**Solution:**
Refresh your token using the `/auth/refresh` endpoint with your refresh token.

### Rate Limit Exceeded During Tests

**Error:**
```
assert response.status_code == 200
AssertionError: assert 429 == 200
```

**Solution:**
The test expects rate limits to be cleared between runs. Check Redis is running and conftest fixture `clear_rate_limits` is resetting it:

```bash
redis-cli FLUSHDB
```

Then rerun tests:
```bash
pytest -v
```

### Weak Password Rejected

**Error:**
```
{
  "error": "Password must contain at least one number"
}
```

**Solution:**
Ensure your password meets the policy:
- At least 8 characters
- At least one letter
- At least one number
- No spaces

Example valid: `Password123`

## Helper Scripts

### set_env.sh - JWT Token Fetcher

This script fetches a JWT token from a running API and optionally saves it to `.env` or exports it to your shell.

**Requirements:** `curl` and `jq` installed.

**Usage:**

1. Interactive save to `.env`:
   ```bash
   ./set_env.sh
   # Answer 'y' when prompted
   ```

2. Export to current shell (ephemeral):
   ```bash
   eval "$(./set_env.sh export)"
   echo $JWT_TOKEN
   ```

3. Manual login without script:
   ```bash
   curl -X POST http://127.0.0.1:8080/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "adminpass"}' | jq .access_token
   ```

**Security Notes:**
- `.env` is git-ignored; do not commit it.
- Tokens are secrets; never share them.
- Prefer ephemeral exports over persistent files for development.
- For production, use a secrets manager (Vault, AWS Secrets Manager).

### setup.sh - Automated Setup

Automated setup script that:
- Updates system packages
- Installs Redis and Python dependencies
- Creates Python venv
- Installs pip packages
- Bootstraps `.env` with seed credentials
- Runs the test suite

**Usage:**
```bash
chmod +x setup.sh
./setup.sh
```

## Future Improvements

### Near-term

- [ ] Implement persistent database (SQLite or PostgreSQL)
- [ ] Add email-based password reset flow
- [ ] Implement token blacklist for logout functionality
- [ ] Add request/response logging and audit trail
- [ ] Improve error messages (generic for security)
- [ ] Add more granular rate limiting (per user, per endpoint)
- [ ] Support multiple resource types (not just tasks)

### Medium-term

- [ ] Add OpenAPI/Swagger documentation
- [ ] Implement request throttling and backoff
- [ ] Add user-level API keys for programmatic access
- [ ] Implement role-based permission system (fine-grained)
- [ ] Add admin dashboard for user management
- [ ] Support file uploads with scan/validation
- [ ] Add webhook support for event notifications

### Long-term

- [ ] Migrate to production WSGI server (Gunicorn, uWSGI)
- [ ] Add Kubernetes deployment manifests
- [ ] Implement GraphQL endpoint alongside REST
- [ ] Add real-time WebSocket support
- [ ] Multi-tenant support
- [ ] Comprehensive monitoring and alerting

## Contributing

This is a personal learning project, but feedback and improvements are welcome:

1. Test thoroughly before submitting changes.
2. Keep security as a priority.
3. Update tests and documentation with code changes.
4. Follow PEP 8 style guide for Python code.

## License

This project is open source and available under the MIT License.

## Contact

For questions or suggestions, open an issue in the repository.

