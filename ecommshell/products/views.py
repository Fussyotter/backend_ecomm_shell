import stripe
import json
import requests

from . import models
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import UpdateAPIView
from django.views import View
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Product.objects.all()
        search_param = self.request.query_params.get('search', None)
        if search_param is not None:
            queryset = queryset.filter(
                Q(title__icontains=search_param) | Q(category__name__icontains=search_param)
            )
        return queryset


def get_random_products(count):
    return Product.objects.order_by('?')[:count]

class ProductDetail(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CategoryItemView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return models.Product.objects.filter(
            category__in=Category.objects.get(
                slug=self.kwargs["slug"]).get_descendants(include_self=True)
        )


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(level=1)
    serializer_class = CategorySerializer


YOUR_DOMAIN = "http://localhost:3000/"


class CreateCheckoutSessionView(View):
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs["slug"])
        stripe.api_key = settings.STRIPE_SECRET_KEY
       # Create a Stripe checkout session
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
                                    'name': product.title,

                        },
                        'unit_amount': int(product.regular_price * 100),


                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:3000',
            cancel_url='http://localhost:8000/cancel/',
        )

       # Render the Stripe checkout page with the session ID
        return JsonResponse({'session_id': session.id, 'product': product.title, 'price': product.regular_price, 'image': product.product_image.all()[0].image.url})


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
                expand=['line_items','shipping_address_collection']
            )

            line_items = session['line_items']
            description = line_items["data"][0]["description"]
            print("--------description ---------->", description)
            quantity = line_items["data"][0]["quantity"]
            print("--------quantity ---------->", quantity)
            session_test = session['customer_details']
            # print("--------shipping ---------->", shipping)
            print("--------line_items ---------->", line_items)
            # print("--------session_test ---------->", session_test)
            update_product(description, quantity)

        else:
            print('Unhandled event type {}'.format(event['type']))

        return HttpResponse(status=200)



@csrf_exempt
def update_product(description, quantity):
    url = f"http://localhost:8000/api/{description}/"
    response = requests.get(url)
    print(response)
    if response.ok:
        product = response.json()
        print(product)
        product["amount"] -= quantity
        serializer = ProductSerializer(data=product)
        if serializer.is_valid():
            data = serializer.validated_data
            response = requests.put(url, json=data)
            if response.ok:
                print("Product updated successfully")
            else:
                print("Product update failed")
        else:
            print("Product serialization failed")

def fulfill_order(line_items):
    # TODO: fill me in
    for line_item in line_items['data']:
        price_data = line_item['price_data']
        product_id = price_data['product_data']['metadata']['product_id']
        print(f"product_id: {product_id}")

        # Retrieve the product with the given product ID
        product = Product.objects.get(id=product_id)
        print(f"product: {product}")

        # Decrement the product quantity by 1
        product.amount -= 1
        product.save()

    # print("Fulfilling order")

    # return redirect(checkout_session.url)
# class CreateCheckoutSessionView(APIView):
#     def post(self, request, *args, **kwargs):
#         product = get_object_or_404(Product, slug=self.kwargs["slug"])

#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=[
#                 'card',
#             ],
#             line_items=[
#                 {
#                     'price_data': {
#                         'currency': 'usd',
#                         'product_data': {
#                             'name': product.title,
#                         },
#                         'unit_amount': int(product.regular_price * 100),
#                     },
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             success_url=YOUR_DOMAIN + reverse('success'),
#             cancel_url=YOUR_DOMAIN + reverse('cancel'),
#         )
#         return JsonResponse({
#             'id': checkout_session.id
#         })
