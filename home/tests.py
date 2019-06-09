from django.test import TestCase

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

# user registration
# user login
# search
# create a reservation
# complete a reservation
