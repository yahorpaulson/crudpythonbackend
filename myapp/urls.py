from django.urls import path
from . import views

urlpatterns= [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('notes', views.note_list_create, name='note_list_create'),
    path ('notes/<int:user_id>', views.notes_get, name='notes_get'),
    path ('notes/<int:user_id>/<int:note_id>', views.notes_get_by_id, name='notes_get_by_id'),
    path ('notes/<int:user_id>/<int:note_id>/delete', views.notes_delete, name='notes_delete'),
]