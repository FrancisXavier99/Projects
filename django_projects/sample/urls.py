from django.urls import path

from . import views

Urlpatterns = [
	path("index", views.index, name="index"),
    path("login",views.login, name="login"),
    path("home",views.home, name="home"),
    path("logout",views.logout, name= "logout"),
]
