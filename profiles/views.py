"""Profile apps vews.py"""
from django.shortcuts import render

from .models import UserProfile

def profile(request):
    """
    Displays the user's profile
    """
    template = 'profiles/profile.html'
    context = {}

    return render(request, template, context)
