from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'id_stripe_public_key': 'pk_test_51MfPedDQVRkRf4r709fW07U9wX6s8Jhrdnu0otDWHLkvU2FjdNpsde4SI4Lv81xA2SANh5TjXmcx9iEgVyPzbEo200ve88Wn2v',
        'client_secret': 'my_super_secret_key_852',
    }

    return render(request, template, context)
