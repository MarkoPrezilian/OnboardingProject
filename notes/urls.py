from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('note', views.note_create, name='note-create'),
    path('note/<str:note_id>', views.note, name='note'),
    path('note-delete/<str:note_id>', views.note_delete, name='note-delete')
]