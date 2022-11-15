from django.test import TestCase
from django.contrib.auth.models import User
from .models import Note
from unittest.mock import patch, Mock

#You need to check redirects

class UserRouteTests(TestCase):
    #How to check if it will redirect to the right route?
    def setUp(self):
        User.objects.create(username='test1', password='1234')
    
    @patch('notes.views.authenticate', return_value=Mock())
    @patch('notes.views.login')
    def test_login_route(self, *mocks):
        #Get login view
        responseView = self.client.get('/login')
        self.assertEqual(responseView.status_code, 200)

        #Login with right username and password
        responseLoginCorrect = self.client.post('/login', {'username': 'test1', 'password': '1234'})
        self.assertEqual(responseLoginCorrect.status_code, 302)
        self.assertEqual(responseLoginCorrect.url, '/dashboard')
        

        #Try to login with wrong password
        responseLoginIncorrect = self.client.post('/login', {'username': 'test1', 'password': '123'})
        self.assertEqual(responseLoginIncorrect.status_code, 302)

        #Check that the logged in user is authenticated
        user = User.objects.get(username='test1')
        self.assertEqual(user.is_authenticated, True)

    def test_signup_route(self):
        #Get Signup view
        responseView = self.client.get('/signup')
        self.assertEqual(responseView.status_code, 200)

        #Signup a new user
        responseSignup = self.client.post('/signup', {'username': 'test2', 'password': '1234'})
        user = User.objects.get(username='test2')
        self.assertEqual(user.username, 'test2')
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(responseSignup.status_code, 302)
        self.assertEqual(responseSignup.url, '/dashboard')

    def test_dashboard_route(self):
        #Get redirected to login if not authenticated
        responseView = self.client.get('/dashboard')
        self.assertEqual(responseView.status_code, 302)
        self.assertEqual(responseView.url, '/login')

        #Get dashboard view
        #First register a user because it also makes it be authenticated
        self.client.post('/signup', {'username': 'test2', 'password': '1234'})
        responseView = self.client.get('/dashboard')
        self.assertEqual(responseView.status_code, 200)
        self.assertEqual(responseView.context['notes'], [])
        self.assertEqual(responseView.context['user'], 'test2')

        #Get dashboard with 2 notes
        self.client.post('/note')
        self.client.post('/note')
        responseView = self.client.get('/dashboard')
        self.assertEqual(len(responseView.context['notes']), 2)
        self.assertEqual(list(responseView.context['notes'])[0].id, 1)



    def test_note_create_route(self):
        #GET request should fail
        responseGet = self.client.get('/note')
        self.assertEqual(responseGet.status_code, 405)

        #POST un-athenticated should fail
        responseFail = self.client.post('/note')
        self.assertEqual(responseFail.status_code, 401)

        #POST authenticated should create a note
        self.client.post('/signup', {'username': 'test2', 'password': '1234'})
        responseNewNote = self.client.post('/note')
        newNote = Note.objects.all()
        self.assertEqual(len(newNote), 1)
        self.assertEqual(responseNewNote.status_code, 302)
        self.assertEqual(responseNewNote.url, '/note/1')
    
    def test_note_delete_route(self):
        #GET request should fail
        responseGet = self.client.get('/note-delete/1')
        self.assertEqual(responseGet.status_code, 405)

        #POST un-authenticated should fail
        responseFail = self.client.post('/note-delete/1')
        self.assertEqual(responseFail.status_code, 401)

        #POST authenticated should delete a note
        self.client.post('/signup', {'username': 'test2', 'password': '1234'})
        responseNewNote = self.client.post('/note')
        newNote = Note.objects.all()
        self.assertEqual(len(newNote), 1)
        self.assertEqual(responseNewNote.status_code, 302)
        responseDelete = self.client.post('/note-delete/1')
        newNote = Note.objects.all()
        self.assertEqual(len(newNote), 0)
        self.assertEqual(responseDelete.status_code, 302)
        self.assertEqual(responseDelete.url, '/dashboard')

    def test_note_route(self):
        #DELETE request should fail
        responseTest = self.client.delete('/note/1')
        self.assertEqual(responseTest.status_code, 405)

        #GET un-authenticated should fail
        responseGetFail = self.client.get('/note/1')
        self.assertEqual(responseGetFail.status_code, 401)
        self.assertEqual(responseGetFail.content, b'User is not authenticated')

        #POST un-authenticated should fail
        responsePostFail = self.client.post('/note/1')
        self.assertEqual(responsePostFail.status_code, 401)
        self.assertEqual(responseGetFail.content, b'User is not authenticated')
        
        #To authenticate
        self.client.post('/signup', {'username': 'test2', 'password': '1234'})

        #GET authenticated should return note view with note
        self.client.post('/note')
        responseView = self.client.get('/note/1')
        self.assertEqual(responseView.status_code, 200)

        #POST authenticated should edit a note
        responseEditNote = self.client.post('/note/1', {'title': 'new nice title', 'content': 'new nice content'})
        editedNote = Note.objects.get(id=1)
        self.assertEqual(responseEditNote.status_code, 302)
        self.assertEqual(editedNote.title, 'new nice title')
        self.assertEqual(editedNote.content, 'new nice content')
        self.assertEqual(responseEditNote.url, '/dashboard')
        
