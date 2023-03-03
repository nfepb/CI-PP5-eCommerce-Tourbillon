"""Views for Product app"""
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category, GenderCategory, ProductStatus, Brand
from .forms import ProductForm


def all_products(request):
    """
    View to return all products.
    It includes sorting and search queries.
    """

    products = Product.objects.all()
    query = None
    categories = None
    gender_categories = None
    product_status = None
    brand = None
    sort = None
    direction = None

    if request.GET:
        if "sort" in request.GET:
            sortkey = request.GET["sort"]
            sort = sortkey
            if sortkey == "name":
                sortkey = "lower_name"
                products = products.annotate(lower_name=Lower("name"))
            if sortkey == "category":
                sortkey = "category__name"
            if sortkey == "gender_category":
                sortkey = "gender_category__name"
            if sortkey == "Product_status":
                sortkey = "Product_status__name"
            if sortkey == "brand":
                sortkey = "brand__name"
            if "direction" in request.GET:
                direction = request.GET["direction"]
                if direction == "desc":
                    sortkey = f"-{sortkey}"
            products = products.order_by(sortkey)

        if "category" in request.GET:
            categories = request.GET["category"].split(",")
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if "gender_category" in request.GET:
            gender_category = request.GET["gender_category"].split(",")
            products = products.filter(
                gender_category__name__in=gender_category)
            gender_categories = (
                GenderCategory.objects.filter(name__in=gender_category))

        if "product_status" in request.GET:
            product_status = request.GET["product_status"].split(",")
            products = products.filter(product_status__name__in=product_status)
            product_status = (
                ProductStatus.objects.filter(name__in=product_status))

        if "q" in request.GET:
            query = request.GET["q"]
            if not query:
                messages.error(
                    request,
                    "You didn't enter any search criteria!")
                return redirect(reverse("products"))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f"{sort}_{direction}"

    # Context to send something back to the template
    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories,
        "current_sorting": current_sorting,
        "current_gender_category": gender_categories,
        "current_product_status": product_status,
        "current_brand": brand,
    }

    return render(request, "products/products.html", context)


def product_details(request, product_id):
    """A view to display the product details"""
    product = get_object_or_404(Product, pk=product_id)

    context = {
        "product": product,
    }

    return render(request, "products/product_details.html", context)


def add_product(request):
    """ Add a product to the store """
    form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
