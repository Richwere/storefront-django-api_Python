from django.urls import path
from . import views


#Url configuration module
urlpatterns = [
    path("hello/", views.say_hello),
]