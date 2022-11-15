from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.shortcuts import render, redirect
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
        notes = list(request.user.note_set.all())
        context['user'] = request.user.username
        context['notes'] = notes
        return render(request, 'notes/dashboard.html', context)
    else:
        return redirect('login')

def note_create(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            note = Note.objects.create(user=user, title='', content='')
            return redirect('/note/' + str(note.id))
        else:
            return HttpResponse('User is not authenticated', status = 401)            
    else:
        return HttpResponseNotAllowed(['POST'])

def note_delete(request, note_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            note = Note.objects.get(id=note_id)
            note.delete()
            return redirect('dashboard')
        else:
            return HttpResponse('User is not authenticated', status = 401)  
    else:
        return HttpResponseNotAllowed(['POST'])

def note(request, note_id):
    context = {}
    if request.method == 'POST':
        if request.user.is_authenticated:
            note = Note.objects.get(id=note_id)
            if note is None:
                return Http404("The note couldn't be found.")
            note.title = request.POST.get('title', note.title)
            note.content = request.POST.get('content', note.content)
            note.save()
            return redirect('/dashboard') #Redirect was adding the string to my URL, so it went from note/id to note/note/id
        else:
            return HttpResponse('User is not authenticated', status = 401)
    elif request.method == 'GET':
        if request.user.is_authenticated:
            note = Note.objects.get(id=note_id)
            context['note'] = note
            return render(request, 'notes/note.html', context)
        else:
            return HttpResponse('User is not authenticated', status = 401)
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])
        
