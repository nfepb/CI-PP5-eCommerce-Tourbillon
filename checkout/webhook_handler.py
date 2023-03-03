from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile

import stripe
import json
import time

class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """

    """
    Init method is called every time an instance of the class
    is created.
    """
    def __init__(self, request):
        """
        Assign the request as an attribute of the class
        in case we want to access the attributes
        """
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email - last added"""
        cust_email = order.email
        # Render both confirmation_emails templates to strings
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            # Context to pass variables to confirmation email:
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            # Context to pass variables to confirmation email:
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event that
        Stripe is sending, returning HTTP response
        """
        intent = event.data.object
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        """
        Replace empty strings with 'None'
        Clean data in the shipping details
        """
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        # Profile set to 'None' for anonymous users to work
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            # Update info if box checked
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.default_county = shipping_details.address.state
                profile.save()

        order_exists = False
        attempt = 1	
        while attempt <= 5:
            try:
                # Check if order exists in database based on fields
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                """
                If order not found, increment attempt by 1 & sleep 1 second.
                Will try to find the order 5 times over 5 seconds.
                """
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                    content=f'Webhook received: {event["type"]} \
                        | SUCCESS: Verified order already in database',
                    status=200
                )

        else:
            order = None
            # If order does not exists, create it
            try:
                # iterate through items in bag from json instead of session
                order = Order.objects.create(
                    # Add user_profile info to order when profile=None
                    # Allow webhook handler to create order for auth users by
                    # attaching to profile
                    user_profile=profile,
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():
                    # Get product ID from bag
                    product = Product.objects.get(id=item_id)
                    # Check if item is integer, item does not have sizes
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            # Quantity will be item data
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        # If item has sizes, iterate through each size
                        # and create line item accordingly
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} \
                | SUCCESS: Created order in webhook',
            status=200
            )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )