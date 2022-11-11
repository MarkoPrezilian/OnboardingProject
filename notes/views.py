from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login

from .models import User, Note


def login(request):
    if request.method == 'GET':
        return render(request, 'notes/login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        test_user = authenticate(request, username=username, password=password)
        print('----------------------------------> ', test_user)
        if username is None:
            raise Http404("Enter username.")
        if password is None:
            raise Http404("Enter password.")

        user = User.objects.get(username=username)
        if user is None:
            raise Http404("The user was not found")

        isValid = check_password(password, user.password)
        if isValid:
            return redirect('dashboard/' + user.username)
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
        hashed_password = make_password(password, salt=None, hasher='default')
        user = User.objects.create(username=username, password=hashed_password)
        return redirect('dashboard/' + str(user.username))


def dashboard(request, username):
    context = {}
    user = User.objects.get(username=username)
    notes = Note.objects.filter(user_id=user.id)
    context['user'] = user.username
    context['notes'] = notes
    return render(request, 'notes/dashboard.html', context)

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
