import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
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
        return JsonResponse({'session_id': session.id,'product':product.title,'price':product.regular_price,'image':product.product_image.all()[0].image.url})


def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None
  try:
    event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Passed signature verification
  return HttpResponse(status=200)
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