"""Context for product app"""
from .models import Product


def products_selected(request):
    """
    A context to display the selected products
    """
    products_selected = Product.objects.filter(featured=True)

    context = {
        "products_selected": products_selected,
    }

    return context


def products_sales(request):
    """
    A context to display the selected products available in stock
    """
    in_stock = Product.objects.filter(product_status__name="in_stock")

    context = {
        "in_stock": in_stock,
    }

    return context
