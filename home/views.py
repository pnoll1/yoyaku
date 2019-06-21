from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import place, reservation
import psycopg2
from django.contrib.gis.gdal import SpatialReference, CoordTransform

def index(request):
    context = {}
    context['static'] = '/static'
    context['restaurant'] = place.objects.all()[:5]
    # search handling
    if request.GET.get('search'):
        # location from geoip2
        search = request.GET.get('search')
        # add geolocation to search, paginate results
        search_result = place.objects.filter(name__icontains=search)
        if search_result:
            context['restaurant'] = search_result
        else:
            context['restaurant']= ''
    # expand restaurant that user clicked on
    if request.GET.get('expand'):
        context['expand'] = request.GET.get('expand')
        context['restaurant'] = place.objects.filter(uuid=request.GET.get('expand'))
        print(context)
        point_qs = list(place.objects.filter(uuid=request.GET.get('expand')))
        for i in point_qs:
            var = i
        location = var.way
        ct = CoordTransform(SpatialReference(3857), SpatialReference(4326))
        location.transform(ct)
        location = location.coords
        print(location)
        context['location'] = location
    # reservation handling
    # reservation form for logged in users, fields prefilled with restaurant data
    if request.GET.get('reserve') and request.user.is_authenticated:
        reserve_place = request.GET.get('reserve')
        context['reserve'] = request.GET.get('reserve')
        context['restaurant'] = place.objects.filter(uuid=reserve_place)
    # freeform reservation
    elif request.GET.get('reserve_freeform') and request.user.is_authenticated:
        return render(request, 'reservation_freeform.html', context)
    # redirect not logged in user to login before reserving
    elif request.GET.get('reserve'):
        messages.error(request, 'You must be logged in to reserve')
        return redirect('/login')
    # reservation form submitted
    if request.GET.get('reservation_submitted'):
        # add validation that reservation at least 30 minutes in future
        context['reservation_submitted'] = request.GET.get('place')
        p = request.GET.get('place')
        phone = request.GET.get('phone')
        name = request.GET.get('name')
        party_size = request.GET.get('party_size')
        time = request.GET.get('time')
        date = request.GET.get('date')
        current_user = request.user
        r = reservation(requested_by_user=current_user.username, phone=phone, name_reservation=name, name_restaurant=p, party_size=party_size, date=date, time=time, request_completed=False)
        try:
            r.full_clean
        except ValidationError as e:
            messages.error('e')
        r.save()
        messages.info(request, "Your reservation is being requested")
    return render(request, 'index.html',context)

def search(request):
    context = {}
    context['static'] = '/static'
    search = request.POST.get('search')
    search_result = point.objects.fiter(name=search)
    if search_result:
        context['restaurant']= search_result
    else:
        context[search_result]= 'Place not found'
    return render(request, 'index.html',context)

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
            meassages.error(request, 'You marked caller but have a user invite code')
        # caller registration
        elif invite_code == invite_code_caller :
            user = User(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            try:
                user.full_clean()
            except ValidationError as e:
                messages.error(request,e)
            if not User.objects.filter(username=username):
                User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                messages.info(request, 'User created')
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

def account(request):
    context = {}
    context['static'] = '/static'
    # caller accounts
    if request.user.is_authenticated and request.user.has_perm('home.can_accept_calls'):
        user = get_user(request)
        context['user'] = user

        context['reservations'] = reservation.objects.filter(Q(request_completed=False), Q(caller='') | Q(caller=user.username))
        if request.POST.get('accepted'):
            uuid = request.POST.get('uuid')
            r = reservation.objects.get(uuid=uuid)
            caller=user.username
            r.caller=caller
            try:
                r.full_clean
            except ValidationError as e:
                messages.error('e')
            r.save()
        if request.POST.get('completed'):
            uuid = request.POST.get('uuid')
            r = reservation.objects.get(uuid=uuid)
            r.request_completed=True
            try:
                r.full_clean
            except ValidationError as e:
                messages.error('e')
            r.save()
        return render(request, 'account_caller.html', context)
    # user accounts
    elif request.user.is_authenticated:
        user = get_user(request)
        context['user'] = get_user(request)
        context['reservations'] = reservation.objects.filter(Q(requested_by_user=user.username), Q(request_completed=False))
        # update reservation
        if request.method == 'POST':
            uuid = request.POST.get('uuid')
            if request.POST.get('cancel'):
                r = reservation.objects.get(uuid=uuid)
                r.delete()
                messages.info(request,'Reservation Deleted')
                return render(request, 'account.html',context)
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
                r.full_clean
            except ValidationError as e:
                messages.error('e')
            r.save()
            messages.info(request,'Reservation updated')
            return render(request, 'account.html',context)
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
#
# translators use admin interface
