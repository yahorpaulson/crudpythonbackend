from django.urls import path
from . import views

urlpatterns= [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('notes', views.show_notes, name='notes'),
    path('create_note', views.create_note, name='create_note'),
    path('add_note', views.add_note, name='add_note'),
    path('delete_note', views.deleteNoteByTitle, name='deleteNoteByTitle'),
    path('refresh', views.refresh_token, name='refresh_token'),
    path('', views.main_view, name='main'),
]
