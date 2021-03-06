from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('register', views.register),
    path('account', views.account),
    path('support', views.support),
    path('add_place', views.add_place)
]
