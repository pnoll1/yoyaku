from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index),
    path('?search', views.search),
    path('login', views.login),
    path('register', views.register),
    ]
