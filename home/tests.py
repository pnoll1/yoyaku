from django.test import TestCase, Client, SimpleTestCase
from django.contrib.auth.models import User, Group

import requests
from home.models import place

class ViewTests(TestCase):

    def test_paths(self):
        r = requests.get('http://localhost:8000')
        self.assertEqual(r.status_code, 200)
        r = requests.get('http://localhost:8000/login')
        self.assertEqual(r.status_code, 200)
        r = requests.get('http://localhost:8000/boogaliboo')
        self.assertEqual(r.status_code, 404)
        r = requests.get('http://localhost:8000/?search')
        self.assertEqual(r.status_code, 200)
        r = requests.get('http://localhost:8000/?expand')
        self.assertEqual(r.status_code, 200)
        r = requests.get('http://localhost:8000/register')
        self.assertEqual(r.status_code, 200)

class UserTests(TestCase):

    def setUp(self):
        Group.objects.get_or_create(name="callers")

    def test_registration(self):
        '''Implictly checks that registration works by checking for redirect
        '''
        c = Client()
        # user
        response = c.post('/register', {'username':'p', 'email':'pat@desktop.lan', 'password':'password', 'password_confirm':'password','first_name':'p', 'last_name':'n', 'invite_code':'isaac'})
        self.assertRedirects(response, '/login')
        # caller
        response = c.post('/register', {'username':'pcall', 'email':'pat@desktop.lan', 'password':'password', 'password_confirm':'password', 'first_name':'p', 'last_name':'n','caller':'on', 'invite_code':'isaac caller'})
        self.assertRedirects(response, '/login')

# user login
# search
# create a reservation
# complete a reservation
