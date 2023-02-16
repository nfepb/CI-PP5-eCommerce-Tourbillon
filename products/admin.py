""" Admin register"""
from django.contrib import admin
from .models import (
    Product, Brand, Category, GenderCategory,
    ProductStatus
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
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
class BrandAdmin(admin.ModelAdmin):
    """
    Displays the Brand model in the admin panel
    """
    list_display = (
        "friendly_name",
        "name",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Displays the Category model in the admin panel
    """
    list_display = (
        "friendly_name",
        "name",
    )


@admin.register(GenderCategory)
class GenderCategoryAdmin(admin.ModelAdmin):
    """
    Displays the Gender Category model in the admin panel
    """
    list_display = (
        "friendly_name",
        "name",
    )


@admin.register(ProductStatus)
class ProductStatusAdmin(admin.ModelAdmin):
    """
    Displays the Product Status model in the admin panel
    """
    list_display = (
        "friendly_name",
        "name",
    )
