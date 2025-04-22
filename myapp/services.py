from .models import Note, UserTokenPair
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.timezone import now as timezone_now

def create_note(data, user_id):
    data['owner_id'] = user_id
    return Note.objects.create(**data)  # Create a new note with the provided data values


def get_all_notes(user_id):
    return Note.objects.filter(owner_id=user_id) # Retrieve all notes for a specific user by their ID

#TODO: relocate logic of checking user


def generate_token_pair(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }  # Generate JWT token pair for the user

def get_user_by_id(user_id):
    return User.objects.get(id=user_id)  # Retrieve a user by their ID


def validate_user(request):
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        messages.error(request, 'Login first!')
        return redirect('login')
    
    user = get_user_by_token(access_token)
    if not user:
        messages.error(request, 'Session expired! Please login again.')
        return redirect('login')
    
    return user
    
def get_user_by_token(access_token):
    try:
        token_pair = UserTokenPair.objects.get(access=access_token)
        if token_pair.access_expiry < timezone_now():
            return None
        return token_pair.user
    except UserTokenPair.DoesNotExist:
        return None
