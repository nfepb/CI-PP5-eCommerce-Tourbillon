"""Profile apps views.py"""
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order


@login_required
def profile(request):
    """
    Displays the user's profile
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    # When updating profile info
    if request.method == 'POST':
        # instance of profile defined in method
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the \
                form is valid')

    else:
        form = UserProfileForm(instance=profile)
    # Get user's associated orders and return them to template
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def account_overview(request):
    """ Displays the account overview"""
    template = 'profiles/account_overview.html'
    return render(request, template)


@login_required
def order_history(request, order_number):
    """ Displays order history """
    profile = get_object_or_404(UserProfile, user=request.user)
    # get all orders under user name
    orders = profile.orders.all().order_by('-id')
    context = {
        'orders': orders,
        'on_page': True,
    }
    return render(request, 'profiles/order_history.html', context)


@login_required
def order_confirmation(request, order_number):
    """ order confirmation page where user can see order summary"""
    order = get_object_or_404(Order, order_number=order_number)
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}.'
        'A confirmation email was sent on the order date'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def admin_profile(request):
    """ Displays admin account overview"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can do that.')
        return redirect(reverse('home'))

    template = 'profiles/admin_profile.html'
    return render(request, template)


@login_required
def product_management(request):
    """ Display product managment page where admin
    can choose to add category and product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store admins can do that.')
        return redirect(reverse('home'))
    template = 'profiles/product_managment.html'
    return render(request, template)