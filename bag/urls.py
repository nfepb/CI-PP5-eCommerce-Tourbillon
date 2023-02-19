"""URL configuration for bag app"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
]