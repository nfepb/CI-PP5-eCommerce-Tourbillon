""" profiles app urls"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_overview, name='account_overview'),
    path('profile/', views.profile, name='profile'),
    path('order_history/', views.order_history, name='order_history'),
    path('order_confirmation/<order_number>',
         views.order_confirmation, name='order_confirmation'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('product_management/', views.product_management, name='product_management'),
]