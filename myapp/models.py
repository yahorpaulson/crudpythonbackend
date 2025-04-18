from django.db import models

# Create your models here.

class Note(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    color = models.CharField(max_length=7, default='#FFFFFF')  # Default color is white
    owner_id = models.IntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    class Meta:
        db_table = 'notes'


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    

    class Meta:
        db_table = 'users'


class UserTokenPair(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access = models.CharField(max_length=255)
    refresh = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    access_expiry = models.DateTimeField()
    refresh_expiry = models.DateTimeField()
    