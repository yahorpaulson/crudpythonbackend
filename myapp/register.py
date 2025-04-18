import hashlib
from .models import User


def hash_password(raw_password):
    return hashlib.sha256(raw_password.encode()).hexdigest()

def register_user(user_data):
    if(User.objects.filter(username=user_data['username']).exists()):
        raise ValueError("Username already exists")
    if(User.objects.filter(email=user_data['email']).exists()):
        raise ValueError("Email already exists")
    user_data['password'] = hash_password(user_data['password'])
    return User.objects.create(
        username=user_data['username'],
        password=user_data['password'],
        email=user_data['email']
    )  # Register a new user with hashed password and unique username/email