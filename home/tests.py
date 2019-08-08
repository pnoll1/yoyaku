from django.test import TestCase, Client, SimpleTestCase, TransactionTestCase
from django.contrib.auth.models import User, Group
from django.contrib.messages import get_messages
from django.db.models import Q
from home.views import Utc9
import datetime

from home.models import place, reservation

utc9 = Utc9()

class ViewTests(TestCase):

    def test_paths(self):
        c = Client()
        r = c.get('http://localhost:8000')
        self.assertEqual(r.status_code, 200)
        r = c.get('http://localhost:8000/login')
        self.assertEqual(r.status_code, 200)
        r = c.get('http://localhost:8000/boogaliboo')
        self.assertEqual(r.status_code, 404)
        r = c.get('http://localhost:8000/?search')
        self.assertEqual(r.status_code, 200)
        r = c.get('http://localhost:8000/?expand')
        self.assertEqual(r.status_code, 200)
        r = c.get('http://localhost:8000/register')
        self.assertEqual(r.status_code, 200)
        r = c.get('http://localhost:8000/add_place')
        self.assertEqual(r.status_code, 200)

class UserTests(TestCase):

    def setUp(self):
        Group.objects.get_or_create(name="callers")

    def test_registration(self):

        c = Client()
        # user
        response = c.post('/register', {'username':'p', 'email':'pat@desktop.lan', 'password':'password', 'password_confirm':'password','first_name':'p', 'last_name':'n', 'invite_code':'isaac'}, follow=True)
        self.assertContains(response, 'User created')
        # caller
        response = c.post('/register', {'username':'pcall', 'email':'pat@desktop.lan', 'password':'password', 'password_confirm':'password', 'first_name':'p', 'last_name':'n','caller':'on', 'invite_code':'isaac caller'}, follow=True)
        self.assertContains(response, 'User created')
        response = c.get('/logout', follow=True)
        self.assertContains(response, 'Logout Successfull')
        # check created user can login
        response = c.post('/login', {'username':'p','password':'password'},follow=True)
        self.assertContains(response, 'Login Successfull')

class ReservationTest(TestCase):

    def test_reservations(self):

        c = Client()
        date = datetime.datetime.now(utc9).date() + datetime.timedelta(days=1)

        # try to go to reservation page while not logged in
        response = c.get('/', {'reserve':'1829cc1f-6a05-472d-9fd0-62bf77bf1a19'}, follow=True)
        self.assertContains(response, 'You must be logged in to reserve')

        # try to make reservation while not logged in
        response = c.post('/',{'reservation_submitted':'yes','place':'たま平','phone':'123456789','name':'johnny','party_size':3,'date':date,'time':'13:03'}, follow=True)
        self.assertContains(response, '{&#39;requested_by_user&#39;: [&#39;This field cannot be blank.&#39;]}')

        # setup user to make reservations
        response = c.post('/register', {'username':'p', 'email':'pat@desktop.lan', 'password':'password', 'password_confirm':'password','first_name':'p', 'last_name':'n', 'invite_code':'isaac'})
        self.assertRedirects(response, '/login')
        response = c.post('/login', {'username':'p','password':'password'},follow=True)
        self.assertContains(response, 'Login Successfull')

        # Reservation under 30 minutes in future
        response = c.post('/',{'reservation_submitted':'yes','place':'たま平','phone':'123456789','name':'johnny','party_size':3,'date':'2019-08-07','time':'13:03'}, follow=True)
        self.assertContains(response, 'Your reservation must be in the future')
        # valid reservation
        response = c.post('/',{'reservation_submitted':'yes','place':'たま平','phone':'123456789','name':'johnny','party_size':3,'date':date,'time':'13:03'}, follow=True)
        self.assertContains(response, 'Your reservation is being requested')
        # get reservation uuid for above reservation
        reservations = reservation.objects.filter(Q(requested_by_user='p'), Q(request_completed=False))
        for res in reservations:
            uuid = res.uuid
        # update reservation
        response = c.post('/account',{'uuid':uuid,'name_restaurant':'たま平','phone':'123456789','name_reservation':'johnny','party_size':3,'date':date,'time':'15:03'}, follow=True)
        self.assertContains(response, 'Reservation updated')
        # delete reservation
        response = c.post('/account',{'uuid':uuid, 'cancel':'yes'})
        self.assertContains(response, 'Reservation Deleted')

# search
# complete a reservation
