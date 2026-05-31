from werkzeug.security import generate_password_hash


# Generic in-memory database for any resource type
resources = {
    "users": [
        {
            "id": 1,
            "username": "admin",
            "role": "admin",
            "password_hash": generate_password_hash("adminpass")
        },
        {
            "id": 2,
            "username": "john_doe",
            "role": "user",
            "password_hash": generate_password_hash("johnpass")
        }
    ],
    "tasks": [
        {"id": 1, "name": "Complete project", "status": "In Progress"},
        {"id": 2, "name": "Write documentation", "status": "Pending"}
    ]
}
