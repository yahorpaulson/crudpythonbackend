from myapp.models import User
import hashlib

def hash_password(raw_password):
    return hashlib.sha256(raw_password.encode()).hexdigest()


def auth(username, password):
    
    hashed = hash_password(password)
    print(hashed)
    try:
        user = User.objects.get(username=username, password=hashed) #Create a new user with hashed password and unique username/email
        return user
    except User.DoesNotExist:
        return None