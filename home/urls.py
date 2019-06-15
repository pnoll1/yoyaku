from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index),
    path('?search', views.search),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('register', views.register),
    path('account', views.account),
    path('support', views.support),
]
