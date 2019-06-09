from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import place
import psycopg2
from django.contrib.gis.gdal import SpatialReference, CoordTransform

def index(request):
    context = {}
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
        context['restaurant'] = place.objects.filter(name=request.GET.get('expand'))
        point_qs = list(place.objects.filter(name=request.GET.get('expand')))
        for i in point_qs:
            var = i
        location = var.way
        ct = CoordTransform(SpatialReference(3857), SpatialReference(4326))
        location.transform(ct)
        location = location.coords
        context['location'] = location
    # need to login to creatte reservation
    if request.GET.get('reserve') and request.user.is_authenticated:
        reserve_place = request.GET.get('reserve')
        context['reserve'] = request.GET.get('reserve')
        context['restaurant'] = place.objects.filter(name=reserve_place) #likely return multiple, need to find by unique id
    elif request.GET.get('reserve'):
        messages.error(request, 'You must be logged in to reserve')
        return redirect('/login')
    if request.GET.get('reservation_submitted'):
        context['reservation_submitted'] = request.GET.get('place')
        # check form inputs are valid
        context['restaurant'] = ''
    context['static'] = '/static'
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

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    # Successfull login
    if user is not None:
        messages.success(request, 'Login Successfull')
        login(request, user)
        # redirect to page they came from
        redirect('/')
        pass
    # login not yet tried
    elif not username:
        context = {}
        context['static'] = '/static'
        return render(request, 'login.html',context)
    # failed login
    else:
        messages.error(request, 'Login Failed')
        context = {}
        context['static'] = '/static'
        return render(request, 'login.html',context)

def register(request):
    #FormView
    # username exists
    #if password and password_confirm:
    #    if password != password_confirm:
    #        messages.error(request, "Passwords don't match")
    # send confirmation email
    context = {}
    context['static'] = '/static'
    return render(request, 'register.html',context)

def loc(request):
    response.set_cookie(location, loc)


def map(request):
    context = {}
    context['static'] = '/static'
    return render(request, 'map.html',context)
#
# translators use admin interface
