from .utils import get_password_hash

# Mock user database
fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": get_password_hash("adminpassword"),
        "role": "admin",
    },
    "testuser": {
        "username": "testuser",
        "email": "testuser@example.com",
        "hashed_password": get_password_hash("testpassword"),
        "role": "user",
    }
}
