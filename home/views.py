"""views for home app"""
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.conf import settings


def home(request):
    """
    view to return the home page
    """
    context = {
        'on_page': True,
    }
    return render(request, "home/home.html", context)


def index(request):
    """
    View to return the index page
    """
    return render(request, 'home/index.html')
