""" Admin register"""
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (
    Product, Brand, Category, GenderCategory,
    ProductStatus
    )


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    """
    Displays the Product model in the admin panel
    """
    list_display = (
        "sku",
        "brand",
        "name",
        "category",
        "gender_category",
        "has_sizes",
        "price",
        "product_status",
        "featured",
        "in_stock",
    )
    search_fields = ('name', 'brand', 'category',)
    ordering = ('brand',)


@admin.register(Brand)
class BrandAdmin(SummernoteModelAdmin):
    """
    Displays the Brand model in the admin panel
    """
    list_display = (
        "friendly_name",
        "name",
    )


@admin.register(Category)
class CategoryAdmin(SummernoteModelAdmin):
    """
    Displays the Category model in the admin panel
    """
    list_display = (
        "friendly_name",
        "name",
    )


@admin.register(GenderCategory)
class GenderCategoryAdmin(SummernoteModelAdmin):
    """
    Displays the Gender Category model in the admin panel
    """
    list_display = (
        "friendly_name",
        "name",
    )


@admin.register(ProductStatus)
class ProductStatusAdmin(SummernoteModelAdmin):
    """
    Displays the Product Status model in the admin panel
    """
    list_display = (
        "friendly_name",
        "name",
    )
