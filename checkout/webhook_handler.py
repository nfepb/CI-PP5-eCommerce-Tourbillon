from django.http import HttpResponse


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

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        """
        Replace empty strings with 'None'
        Clean data in the shipping details
        """
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1	
        while attempt <= 5:
            try:
                # Check if order exists in database based on fields
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=shipping_details.email,
                    phone__iexact=shipping_details.phone,
                    country__iexact=shipping_details.country,
                    postcode__iexact=shipping_details.postal_code,
                    town_or_city__iexact=shipping_details.city,
                    street_address_1__iexact=shipping_details.line1,
                    street_address_2__iexact=shipping_details.line2,
                    county__iexact=shipping_details.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                    content=f'Webhook received: {event:["type"]} | SUCCESS: Verified order already in database',
                    status=200
                )

        else:
            order = None
            # If order does not exists, create it
            try:
                # iterate through items in bag from json instead of session
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=shipping_details.email,
                    phone=shipping_details.phone,
                    country=shipping_details.country,
                    postcode=shipping_details.postal_code,
                    town_or_city=shipping_details.city,
                    street_address_1=shipping_details.line1,
                    street_address_2=shipping_details.line2,
                    county=shipping_details.state,
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
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
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