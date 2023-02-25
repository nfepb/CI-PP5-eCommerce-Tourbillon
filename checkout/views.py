""" Views for Checkout app"""
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
import stripe

from .forms import OrderForm
from bag.contexts import bag_contents


def checkout(request):
    """ checkout view"""
    # Payment intent based on Stripe variables
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    # Stripe needs amount as integer
    stripe_total = round(total * 100)
    # Set secret key on Stripe
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    print(intent)

    order_form = OrderForm()
    if not stripe_public_key:
        messages.warning(
            request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?'
            )
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': stripe_secret_key,
    }

    return render(request, template, context)
