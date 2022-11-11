from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('note', views.noteModify, name='note-create'),
    path('note/<int:note_id>', views.note, name='note')
]