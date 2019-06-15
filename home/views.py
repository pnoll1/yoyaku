from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import place, reservation
import psycopg2
from django.contrib.gis.gdal import SpatialReference, CoordTransform

def index(request):
    context = {}
    context['static'] = '/static'
    context['restaurant'] = place.objects.all()[:5]
    if request.GET.get('search'):
        # location from geoip2
        search = request.GET.get('search')
        # add geolocation to search, paginate results
        search_result = place.objects.filter(name__icontains=search)
        if search_result:
            context['restaurant'] = search_result
        else:
            context['restaurant']= ''
    if request.GET.get('expand'):
        context['expand'] = request.GET.get('expand')
        # use uuid for lookup, keep search results and only expand selected one ideally
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
    # need to login to create reservation
    if request.GET.get('reserve') and request.user.is_authenticated:
        reserve_place = request.GET.get('reserve')
        context['reserve'] = request.GET.get('reserve')
        context['restaurant'] = place.objects.filter(uuid=reserve_place)
    # freeform reservation
    elif request.GET.get('reserve_freeform') and request.user.is_authenticated:
        return render(request, 'reservation_freeform.html', context)
    elif request.GET.get('reserve'):
        messages.error(request, 'You must be logged in to reserve')
        return redirect('/login')
    if request.GET.get('reservation_submitted'):
        context['reservation_submitted'] = request.GET.get('place')
        p = request.GET.get('place')
        name = request.GET.get('name')
        party_size = request.GET.get('party_size')
        time = request.GET.get('time')
        date = request.GET.get('date')
        current_user = request.user
        r = reservation(requested_by_user=current_user,name_reservation=name, name_restaurant=p, party_size=party_size, date=date, time=time, request_completed=False)
        try:
            r.full_clean
        except ValidationError as e:
            messages.error('e')
        r.save()
    elif request.GET.get('reservation_freeform_submitted'):
        context['reservation_submitted'] = request.GET.get('place')
        p = request.GET.get('place')
        phone = request.GET.get('phone')
        name = request.GET.get('name')
        party_size = request.GET.get('party_size')
        time = request.GET.get('time')
        date = request.GET.get('date')
        current_user = request.user
        r = reservation(requested_by_user=current_user, phone=phone, name_reservation=name, name_restaurant=p, party_size=party_size, date=date, time=time, request_completed=False)
        try:
            r.full_clean()
        except ValidationError as e:
            messages.error('e')
        r.save()
        context['restaurant'] = ''
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
    # login not yet tried
    elif request.user.is_authenticated and request.method == 'GET':
        messages.info(request, "You're already logged in")
        return redirect('/')
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
        elif invite_code == invite_code_user and caller:
            meassages.error(request, 'You marked caller but have a user invite code')
        elif invite_code == invite_code_caller : # not working
            user = User(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            try:
                user.full_clean()
            except ValidationError as e:
                messages.error(request,e)
            if not User.objects.filter(username=username):
                User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                messages.info(request, 'User created')
                group = Group.objects.get(name="callers")
                #group.user_set.add(user)
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
    if request.user.is_authenticated and request.user.has_perm('reservation.can_accept_calls'):
        context['user'] = user
        context['reservations'] = reservation.objects.filter(caller='')
    elif request.user.is_authenticated:
        user = get_user(request)
        print('not caller')
        context['user'] = get_user(request)
        context['reservations'] = reservation.objects.filter(requested_by_user=user.username)
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
