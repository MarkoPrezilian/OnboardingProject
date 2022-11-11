from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import Note


def login_view(request):
    if request.method == 'GET':
        return render(request, 'notes/login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('login')


def signup(request):
    if request.method == 'GET':
        return render(request, 'notes/signup.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is None or password is None:
            raise Http404("Username or password is missing.")
        user = User.objects.create_user(username, '', password)
        login(request, user)      
        return redirect('dashboard')


def dashboard(request):
    context = {}
    if request.user.is_authenticated:
        notes = Note.objects.filter(user_id=request.user.id)
        context['user'] = request.user.username
        context['notes'] = notes
        return render(request, 'notes/dashboard.html', context)
    else:
        return redirect('login')

def noteModify(request):
    if request.method == 'POST':
        user = User.objects.get(username='marko')
        note = Note.objects.create(user=user, title='', content='')
        return redirect('/note/' + str(note.id))
    

def note(request, note_id):
    context = {}
    if request.method == 'GET':
        note = Note.objects.get(id=note_id)
        context['note'] = note
        return render(request, 'notes/note.html', context)
    elif request.method == 'POST':
        note = Note.objects.get(id=note_id)
        if note is None:
            return HttpResponse("Couldn't update the note, sorry.") #Is there a 500 error way?
        note.title = request.POST.get('title', note.title)
        note.content = request.POST.get('content', note.content)
        note.save()
        return redirect('http://127.0.0.1:8000/note/' + str(note.id)) #Redirect was adding the string to my URL, so it went from note/id to note/note/id
    elif request.method == 'DELETE':
        note = Note.objects.get(id=note_id)
        note.delete()
        return redirect('dashboard/marko')
