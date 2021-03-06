from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import place, reservation, place_staging
import psycopg2
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import Point
import datetime
import re

# Japan timezone class
class Utc9(datetime.tzinfo):
    _offset = datetime.timedelta(hours=9)
    _dst = datetime.timedelta(0)
    def utcoffset(self,dt):
        return self.__class__._offset
    def dst(self, dt):
        return self.__class__._dst

utc9 = Utc9()

# restaurant search
def search(request):
    context = {}
    context['static'] = '/static'
    search = request.GET.get('search')
    search_result = place.objects.filter(name__icontains=search)
    if search_result:
        context['restaurant']= search_result
    else:
        context['restaurant']= ''
    return render(request, 'index.html',context)

def restaurant_location_to_4326(uuid):
    point_qs = list(place.objects.filter(uuid=uuid))
    for i in point_qs:
        var = i
    location = var.way
    ct = CoordTransform(SpatialReference(3857), SpatialReference(4326))
    location.transform(ct)
    location = location.coords
    return location

def index(request):
    context = {}
    context['static'] = '/static'
    #context['restaurant'] = place.objects.all()[:5]
    # expand restaurant that user clicked on
    if request.GET.get('expand'):
        context['expand'] = request.GET.get('expand')
        context['restaurant'] = place.objects.filter(uuid=request.GET.get('expand'))
        context['location'] = restaurant_location_to_4326(request.GET.get('expand'))
        return render(request, 'index.html', context)
    if request.GET.get('search'):
        return search(request)
    # blank reservation form on first load
    if request.method == "GET" and not request.GET.get('reserve') and request.user.is_authenticated:
        context['restaurant'] = ''
        context['date'] = datetime.datetime.now(utc9).date()
        return render(request, 'reservation.html', context)
    if request.method == "GET" and not request.GET.get('reserve'):
        messages.error(request, 'You must be logged in to reserve')
        return redirect('/login')
    # reservation handling
    # reservation form for logged in users, fields prefilled with restaurant data
    if request.method == "GET" and request.GET.get('reserve') and request.user.is_authenticated:
        reserve_place = request.GET.get('reserve')
        context['reserve'] = request.GET.get('reserve')
        context['restaurant'] = place.objects.filter(uuid=reserve_place)
        context['date'] = datetime.datetime.now(utc9).date()
        return render(request, 'reservation.html', context)
    # freeform reservation
    elif request.method == "GET" and request.GET.get('reserve_freeform') and request.user.is_authenticated:
        context['restaurant'] = ''
        context['date'] = datetime.datetime.now(utc9).date()
        return render(request, 'reservation.html', context)
    # redirect not logged in user to login before reserving
    elif request.method == "GET" and request.GET.get('reserve') or request.method == "GET" and request.GET.get('reserve_freeform'):
        messages.error(request, 'You must be logged in to reserve')
        return redirect('/login')
    # reservation form submitted
    if request.method=="POST":
        # add validation that reservation at least 30 minutes in future
        context['reservation_submitted'] = request.POST.get('place')
        p = request.POST.get('place')
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        party_size = request.POST.get('party_size')
        time = request.POST.get('time')
        date = request.POST.get('date')
        current_user = request.user
        r = reservation(requested_by_user=current_user.username, phone=phone, name_reservation=name, name_restaurant=p, party_size=party_size, date=date, time=time, request_completed=False)
        # validate reservation date and time
        date = datetime.date.fromisoformat(date)
        time = datetime.time.fromisoformat(time)
        d = datetime.datetime.combine(date,time,utc9)
        if (datetime.datetime.now(utc9) - datetime.timedelta(minutes=30)) > d:
            messages.error(request, 'Your reservation must be in the future')
            return render(request, 'index.html',context)
        # validate phone number starts with + and has 11-13 digits(11 is geographic numbers, 13 is not geographic)
        #if not re.fullmatch(r'^[+]\d{11-13}',phone):
        #    messages.error(request, 'You must give full number with country code including +')
        #    return render(request, 'index.html',context)
        try:
            r.full_clean()
        except ValidationError as e:
            messages.error(request, e)
            return render(request, 'index.html', context)
        r.save()
        # send data to add_place page
        if request.POST.get('place_in_db'):
            messages.info(request, "Your reservation is being requested")
            add_place_and_queries = '/add_place' + '?name=' + p + '&phone=' + phone
            return redirect(add_place_and_queries)
        messages.info(request, "Your reservation is being requested")
    return render(request, 'index.html',context)

def add_place(request):
    context = {}
    context['static'] = '/static'
    # give center point for map
    context['location'] = restaurant_location_to_4326('1143bb6c-7b58-4c16-80ff-08bfa59dcda3')
    # place succesfully added
    if request.GET.get('success')=='yes':
        messages.info(request, 'Thanks for helping us improve! Place will be added after verification')
        return redirect('/')
    # place not added, add message and reload page with info
    elif request.GET.get('success')=='no':
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        context['name'] = name
        context['phone'] = phone
        messages.info(request, 'Place not added, did you select a location?')
        return render(request, 'add_place.html' , context)
    current_user = request.user
    name = request.GET.get('name')
    phone = request.GET.get('phone')
    context['name'] = name
    context['phone'] = phone
    # get lat, long and translate for saving in db
    queries = request.GET.dict()
    if 'place_loc' in queries.keys():
        place_loc = queries['place_loc']
        place_loc = place_loc.split(',')
        n=0
        for i in place_loc:
            place_loc[n]=float(i)
            n += 1
        place_point = Point(place_loc)
        ct = CoordTransform(SpatialReference(4326), SpatialReference(3857))
        place_point.transform(ct)
        p = place_staging(requested_by_user=current_user, name=name, phone=phone, way=place_point)
        try:
            p.full_clean()
        except ValidationError as e:
            messages.error(request, e)
            return render(request, 'add_place.html',context)
        p.save()
    return render(request, 'add_place.html',context)

def login_view(request):
    context = {}
    context['static'] = '/static'
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    # Successfull login
    if user is not None and request.method == 'POST':
        login(request, user)
        messages.success(request, 'Login Successfull')
        # redirect to page they came from
        return redirect('/')
    # redirect logged in user
    elif request.user.is_authenticated and request.method == 'GET':
        messages.info(request, "You're already logged in")
        return redirect('/')
    # login not yet tried
    elif request.method == 'GET' and user is None:
        return render(request, 'login.html',context)
    # failed login
    else:
        messages.error(request, 'Login Failed')
        return render(request, 'login.html',context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout Successfull')
    return redirect('/')

def register(request):
    # check if form views be better
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    caller = request.POST.get('caller')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')
    invite_code = request.POST.get('invite_code')
    if username and email and password and password_confirm and invite_code:
        if password != password_confirm:
            messages.error(request,"The password fields must match")
        invite_code = request.POST.get('invite_code')
        invite_code_caller = 'isaac caller'
        invite_code_user = 'isaac'
        # user registration handling
        if invite_code == invite_code_user and not caller:
            user = User(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            try:
                user.full_clean()
            except ValidationError as e:
                messages.error(request,e)
            if not User.objects.filter(username=username):
                User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                messages.info(request, 'User created')
                return redirect('/login')
            messages.error(request, 'Username taken')
        # user tries to mark as caller
        elif invite_code == invite_code_user and caller:
            messages.error(request, 'You marked caller but have a user invite code')
        # caller registration
        elif invite_code == invite_code_caller :
            user = User(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            try:
                user.full_clean()
            except ValidationError as e:
                messages.error(request,e)
                return render(request, 'register.html',context)
            if not User.objects.filter(username=username):
                User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                messages.info(request, 'User with caller permissions created')
                group = Group.objects.get(name="callers")
                user = User.objects.get(username=username)
                user.groups.add(group)
                return redirect('/login')
    else:
        messages.error(request, 'Fields missing')
    # send confirmation email
    context = {}
    context['static'] = '/static'
    return render(request, 'register.html',context)

# Update
# Cancel
# accept revised time
def account(request):
    context = {}
    context['static'] = '/static'
    # caller accounts
    if request.user.is_authenticated and request.user.has_perm('home.can_accept_calls'):
        user = get_user(request)
        context['user'] = user
        context['accepted_reservations'] = reservation.objects.filter(caller=user.username)
        context['reservations'] = reservation.objects.filter(Q(request_completed=False), Q(caller=''))
        context['my_reservations'] = reservation.objects.filter(Q(requested_by_user=user.username), Q(request_completed=False))
        # update personal reservations
        if request.POST.get('name_restaurant'):
            uuid = request.POST.get('uuid')
            name_restaurant = request.POST.get('name_restaurant')
            phone = request.POST.get('phone')
            name_reservation = request.POST.get('name_reservation')
            party_size = request.POST.get('party_size')
            time = request.POST.get('time')
            date = request.POST.get('date')
            r = reservation.objects.get(uuid=uuid)
            if r.caller:
                messages.error(request, 'Your reservation has been or is being made. Updating is not allowed')
                return render(request, 'account.html',context)
            r.name_restaurant = name_restaurant
            r.phone = phone
            r.name_reservation = name_reservation
            r.party_size = party_size
            r.time = time
            r.date = date
            try:
                r.full_clean()
            except ValidationError as e:
                messages.error(request, e)
                return render(request, 'account.html',context)
            r.save()
            messages.info(request,'Reservation Updated')
            return render(request, 'account.html',context)
        # accepted work
        if request.POST.get('accepted'):
            uuid = request.POST.get('uuid')
            r = reservation.objects.get(uuid=uuid)
            caller=user.username
            r.caller=caller
            try:
                r.full_clean()
            except ValidationError as e:
                messages.error(request, e)
                return render(request, 'account_caller.html', context)
            r.save()
            messages.success(request, 'Work Accepted')
        # original time doesn't work
        if request.POST.get('new_time_needed'):
            uuid = request.POST.get('uuid')
            context['date_today'] = datetime.datetime.now(utc9).date()
            context['new_time_needed'] = 'yes'
            context['uuid'] = uuid
            return render(request, 'account_caller.html', context)
        # caller inputs possible times from restaurant
        if request.POST.get('acceptable_time'):
            uuid = request.POST.get('uuid')
            acceptable_date = request.POST.get('acceptable_date')
            acceptable_time = request.POST.get('acceptable_time')
            acceptable_date = datetime.date.fromisoformat(acceptable_date)
            acceptable_time = datetime.time.fromisoformat(acceptable_time)
            d = datetime.datetime.combine(acceptable_date,acceptable_time,utc9)
            # time validation
            r = reservation.objects.get(uuid=uuid)
            r.acceptable_time = d
            try:
                r.full_clean()
            except ValidationError as e:
                messages.error(request, e)
                return render(request, 'account_caller.html', context)
            r.save()
            messages.success(request, 'Reservation Updated')
        # accept revised time
        if request.POST.get('accepted_time'):
            uuid = request.POST.get('uuid')
            accepted_time = request.POST.get('accepted_time')
            accepted_time = accepted_time.replace('_', ' ')
            r = reservation.objects.get(uuid=uuid)
            r.accepted_time = accepted_time
            try:
                r.full_clean()
            except ValidationError as e:
                messages.error(request, e)
                return render(request, 'account_caller.html', context)
            r.save()
            messages.success(request, 'Reservation Updated')
        # reservation completed
        if request.POST.get('completed'):
            uuid = request.POST.get('uuid')
            r = reservation.objects.get(uuid=uuid)
            r.request_completed=True
            try:
                r.full_clean()
            except ValidationError as e:
                messages.error(request, e)
                return render(request, 'account_caller.html', context)
            r.save()
        # cancel reservation
        if request.POST.get('cancel'):
            uuid = request.POST.get('uuid')
            r = reservation.objects.get(uuid=uuid)
            r.delete()
            messages.info(request,'Reservation Deleted')
            return render(request, 'account.html',context)
        # show reservation details
        if request.GET.get('expand'):
            context['expand'] = request.GET.get('expand')
            return render(request, 'account_caller.html',context)
        return render(request, 'account_caller.html', context)
    # user accounts
    elif request.user.is_authenticated:
        user = get_user(request)
        context['user'] = get_user(request)
        context['my_reservations'] = reservation.objects.filter(Q(requested_by_user=user.username), Q(request_completed=False))
        # update reservation
        if request.method == 'POST' and request.POST.get('name_restaurant'):
            uuid = request.POST.get('uuid')
            name_restaurant = request.POST.get('name_restaurant')
            phone = request.POST.get('phone')
            name_reservation = request.POST.get('name_reservation')
            party_size = request.POST.get('party_size')
            time = request.POST.get('time')
            date = request.POST.get('date')
            r = reservation.objects.get(uuid=uuid)
            if r.caller:
                messges.error(request, 'Your reservation has been or is being made. Updating is not allowed')
                return render(request, 'account.html',context)
            r.name_restaurant = name_restaurant
            r.phone = phone
            r.name_reservation = name_reservation
            r.party_size = party_size
            r.time = time
            r.date = date
            try:
                r.full_clean()
            except ValidationError as e:
                messages.error(request, e)
                return render(request, 'account.html',context)
            r.save()
            messages.info(request,'Reservation Updated')
            return render(request, 'account.html',context)
        if request.POST.get('cancel'):
            uuid = request.POST.get('uuid')
            r = reservation.objects.get(uuid=uuid)
            r.delete()
            messages.info(request,'Reservation Deleted')
            return render(request, 'account.html',context)
        # accept revised time
        if request.POST.get('accepted_time'):
            uuid = request.POST.get('uuid')
            accepted_time = request.POST.get('accepted_time')
            accepted_time = accepted_time.replace('_', ' ')
            r = reservation.objects.get(uuid=uuid)
            r.accepted_time = accepted_time
            try:
                r.full_clean()
            except ValidationError as e:
                messages.error(request, e)
                return render(request, 'account.html', context)
            r.save()
            messages.success(request, 'Reservation Updated')
        # show reservation details
        if request.GET.get('expand'):
            context['expand'] = request.GET.get('expand')
            return render(request, 'account.html',context)
    # logged out users
    else:
        messages.info(request,"You're not logged in")
        return redirect('/')
    return render(request, 'account.html',context)

def support(request):
    context = {}
    context['static'] = '/static'
    return render(request, 'support.html',context)

def map(request):
    context = {}
    context['static'] = '/static'
    return render(request, 'map.html',context)
