import os
from werkzeug.security import generate_password_hash


SEED_ADMIN_PASSWORD = os.getenv("SEED_ADMIN_PASSWORD")
SEED_USER_PASSWORD = os.getenv("SEED_USER_PASSWORD")


# Generic in-memory database for any resource type
resources = {
    "users": [
        {
            "id": 1,
            "username": "admin",
            "role": "admin",
            "password_hash": generate_password_hash(SEED_ADMIN_PASSWORD) if SEED_ADMIN_PASSWORD else ""
        },
        {
            "id": 2,
            "username": "john_doe",
            "role": "user",
            "password_hash": generate_password_hash(SEED_USER_PASSWORD) if SEED_USER_PASSWORD else ""
        }
    ],
    "tasks": [
        {"id": 1, "name": "Complete project", "status": "In Progress"},
        {"id": 2, "name": "Write documentation", "status": "Pending"}
    ]
}
