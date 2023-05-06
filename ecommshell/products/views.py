import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework import generics
from django.views import View
from . import models
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveAPIView):
    lookup_field = "slug"
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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
        metadata = {'product_id': str(product.id)}
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {
                                    'name': product.title,
                                    'metadata': metadata,

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
        print(f"metadata: {metadata}")

       # Render the Stripe checkout page with the session ID
        return JsonResponse({'session_id': session.id,'product':product.title,'price':product.regular_price,'image':product.product_image.all()[0].image.url})


class WebHook(View):
    def post(self, request):
        event = None
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_SECRET_WEBHOOK
            )
        except ValueError as err:
            # Invalid payload
            raise err
        except stripe.error.SignatureVerificationError as err:
            # Invalid signature
            raise err

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            print("--------payment_intent ---------->", payment_intent)
        elif event.type == 'payment_method.attached':
            payment_method = event.data.object
            print("--------payment_method ---------->", payment_method)
        # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event.type))
        return JsonResponse(success=True, safe=False)

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