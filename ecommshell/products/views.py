import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from rest_framework import generics
from django.views import View
from rest_framework.views import APIView
from . import models
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.shortcuts import get_object_or_404


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
        session = stripe.checkout.Session.create(
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
           success_url='http://localhost:8000/success/',
           cancel_url='http://localhost:8000/cancel/',
       )
       # Render the Stripe checkout page with the session ID
        return JsonResponse({'session_id': session.id})

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