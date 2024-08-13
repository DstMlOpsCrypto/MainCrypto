from .utils import get_password_hash

# Mock user database
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@example.com",
        "hashed_password": get_password_hash("adminpassword"),
        "role": "admin",
    },
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "hashed_password": get_password_hash("testpassword"),
        "role": "user",
    }
}
