from .models import Note
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def create_note(data, user_id):
    data['owner_id'] = user_id
    return Note.objects.create(**data)  # Create a new note with the provided data values


def get_all_notes(user_id):
    return Note.objects.filter(owner_id=user_id) # Retrieve all notes for a specific user by their ID

#TODO: logic of checking user


def generate_token_pair(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }  # Generate JWT token pair for the user

def get_user_by_id(user_id):
    return User.objects.get(id=user_id)  # Retrieve a user by their ID
