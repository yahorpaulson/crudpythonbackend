from django import forms
from .models import Note, User


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'color', 'owner_id']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Content'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
            'owner_id': forms.HiddenInput(),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }