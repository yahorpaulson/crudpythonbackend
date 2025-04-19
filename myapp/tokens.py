import uuid
from .models import UserTokenPair
from django.utils.timezone import now as timezone_now
from datetime import timedelta


def create_token_pair(user):
    access = str(uuid.uuid4()) # generate token and tramsform to string
    refresh = str(uuid.uuid4()) 

    access_expiry = timezone_now() + timedelta(minutes=15) # set access token expiry time to 15 minutes from now

    refresh_expiry = timezone_now() + timedelta(days=7) 


    UserTokenPair.objects.create(
        user=user,
        access=access,
        refresh=refresh,
        access_expiry=access_expiry,
        refresh_expiry=refresh_expiry
    )  # Create a new token pair for the user

    return {
        'access': access,
        'refresh': refresh,
        'access_expiry': access_expiry,
        'refresh_expiry': refresh_expiry
    }



def refresh_access_token(refresh_token):
    try:
        token = UserTokenPair.objects.get(refresh=refresh_token)  # Retrieve the token pair using the refresh token
        if token.refresh_expiry < timezone_now():  # Check if the refresh token has expired
            raise Exception("Refresh token expired")
        

        new_access = str(uuid.uuid4())
        new_expiry = timezone_now() + timedelta(minutes=15)


        token.access = new_access  # Update the access token
        token.access_expiry = new_expiry  # Update the access token expiry time
        token.save()

        return {
            'access': new_access,
            'access_expiry': new_expiry
        }  # Return the new access token and its expiry time
    except UserTokenPair.DoesNotExist:
        raise Exception("Invalid refresh token")
    except Exception as e:
        raise Exception(f"Error refreshing access token: {str(e)}")
    

def delete_token_pair(user_id):
    try:
        token = UserTokenPair.objects.get(user_id=user_id)  # Retrieve the token pair using the user ID
        token.delete()
    except UserTokenPair.DoesNotExist:
        raise Exception("Token pair does not exist")
    

def get_user_by_token(access_token):
    try:
        token_pair = UserTokenPair.objects.get(access=access_token)
        return token_pair.user
    except UserTokenPair.DoesNotExist:
        return None

