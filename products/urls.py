"""Product app URLs"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_products, name="products"),
    path("<int:product_id>/", views.product_details, name="product_details"),
    path("add/", views.add_product, name="add_product"),
    path("edit/<int:product_id>/", views.edit_product, name="edit_product"),
    path("delete/<int:product_id>/", views.delete_product,
         name="delete_product"),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:category_id>/',
         views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/',
         views.delete_category, name='delete_category'),
     path(
        'edit_review/<int:review_id>/',
        views.edit_review, name='edit_review'),
    path(
        'delete_review/<int:review_id>/',
        views.delete_review, name='delete_review'),

]