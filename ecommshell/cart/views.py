import stripe
import json
import requests

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartItemSerializer, CartSerializer
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views import View
from django.http import HttpResponseForbidden

# @method_decorator(login_required, name='dispatch')
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]  

    serializer_class = CartItemSerializer  

    def post(self, request, product_id): 
        cart, created = Cart.objects.get_or_create(user=request.user)

        product = get_object_or_404(Product, id=product_id)
        quantity = request.data.get('quantity', 1)

        cart.add_product(product, quantity)

        response_data = {
            'success': True,
            'message': f"{product.title} added to cart.",
            'cart_total': cart.calculate_total(),
        }

        return Response(response_data, status=status.HTTP_200_OK)


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)   


class CreateCheckoutSessionView(View):
    queryset = Cart.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('You must be logged in to view this page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        YOUR_DOMAIN = "http://localhost:3000"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            shipping_address_collection={"allowed_countries": ["US", "CA"]},
            shipping_options=[
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 0, "currency": "usd"},
                        "display_name": "Free shipping",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 5},
                            "maximum": {"unit": "business_day", "value": 7},
                        },
                    },
                },
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 1500, "currency": "usd"},
                        "display_name": "Next day air",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 1},
                            "maximum": {"unit": "business_day", "value": 1},
                        },
                    },
                },
            ],
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.title,
                        },
                        'unit_amount': int(item.product.regular_price * 100),
                    },
                    'quantity': item.quantity,
                }
                for item in cart.items.all()
            ],
            mode='payment',
            success_url='http://localhost:3000',
            cancel_url='http://localhost:8000/cancel/',
        )
        return JsonResponse({'id': session.id})


@method_decorator(csrf_exempt, name='dispatch')
class WebHook(View):
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        webhook_secret = settings.STRIPE_SECRET_WEBHOOK
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None
        # print("--------payload ---------->", payload)

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as err:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as err:
            # Invalid signature
            return HttpResponse(status=400)
        # Handle the checkout.session.completed event
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        if event['type'] == 'checkout.session.completed':
            session = stripe.checkout.Session.retrieve(
                event['data']['object']['id'],
                expand=['line_items', 'shipping_address_collection']
            )

            line_items = session['line_items']['data']
            for item in line_items:
                description = item["description"]
                quantity = item["quantity"]
                print("--------description ---------->", description)
                print("--------quantity ---------->", quantity)
            session_test = session['customer_details']
            # print("--------shipping ---------->", shipping)
            print("--------line_items ---------->", line_items)
            # print("--------session_test ---------->", session_test)
        else:
            print('Unhandled event type {}'.format(event['type']))

        return HttpResponse(status=200)
