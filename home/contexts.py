"""context.py for home app"""
from products.models import Category


def product_categories(request):
    """
    Provides global access to categories
    """
    categories = Category.objects.all().order_by('friendly_name')

    context = {
        'categories': categories,
    }

    return 