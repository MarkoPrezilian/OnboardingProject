from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('dashboard/<str:username>', views.dashboard, name='dashboard'),
    path('note', views.noteModify, name='note-create'),
    path('note/<int:note_id>', views.note, name='note')
]