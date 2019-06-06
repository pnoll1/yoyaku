from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import place
import psycopg2
from .models import planet_osm_point as point
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.measure import D, Distance
from django.contrib.gis.geos import GEOSGeometry, Point
from itertools import chain



def index(request):
    context = {}
    #conn = psycopg2.connect("dbname='reservation' user='pat' host='127.0.0.1' password='password'")
    #cur=conn.cursor()
    #cur.execute("SELECT osm_id,name FROM planet_osm_point LIMIT 5;")
    #rows = cur.fetchall()
    #context['restaurant'] = rows
    # list a few restaurants (preferably near location)
    context['restaurant'] = point.objects.all()[:5]
    if request.GET.get('search'):
        # location from geoip2
        search = request.GET.get('search')
        # add geolocation to search, paginate results
        #location_current = Point(136.84988469999996, 35.05016499965509,srid = 4326) #domes kitchen
        #dome = point.objects.get(name="Dome's Kitchen")
        #location_current = fromstr('POINT(136.84988469999996 35.05016499965509)',srid = 4326) #domes kitchen
        #ct = CoordTransform(SpatialReference(4326), SpatialReference(3857))
        #location_current.transform(ct)
        search_result = point.objects.filter(name__icontains=search)
        #search_result_dist = []
        #for i in search_result:
        #    c =0
        #    shit = i.way.distance(location_current)
        #    print(shit)
        #print(search_result_dist)
        # filter by location
        #search_result_spatial = point.objects.filter(way__distance_lt=(dome.way, D(m=5), 'spheroid'))#.annotate(distance=Distance(dome.way, field_name='way')).order_by('distance')
        #search_result = list(chain(search_result,search_result_spatial))
        #search_result = point.objects.filter(location_current__distance_lte=(way, D(mi=15))) #.distance(location_current, field_name='seller_current_location').order_by('distance')[:10]
        if search_result:
            context['restaurant'] = search_result
        else:
            context['restaurant']= ''
    if request.GET.get('expand'):
        context['expand'] = request.GET.get('expand')
        # use uuid for lookup, keep search results and only expand selected one ideally
        context['restaurant'] = point.objects.filter(name=request.GET.get('expand'))
        # get coords of restaurant and transform for leaflet usage
        location_current = GEOSGeometry('Point(136.84988469999996 35.05016499965509)',srid = 4326) #domes kitchen
        ct = CoordTransform(SpatialReference(4326), SpatialReference(3857))
        location_current.transform(ct)
        print(location_current.coords)
        point_qs = list(point.objects.filter(name=request.GET.get('expand')))
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
        context['restaurant'] = point.objects.filter(name=reserve_place) #likely return multiple, need to find by unique id
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
