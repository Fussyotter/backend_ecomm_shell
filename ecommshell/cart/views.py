from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartItemSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@csrf_exempt
@login_required
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)

    product = get_object_or_404(Product, id=product_id)
    quantity = request.POST.get('quantity', 1)

    cart.add_product(product, quantity)

    response_data = {
        'success': True,
        'message': f"{product.title} added to cart.",
        'cart_total': cart.calculate_total(),
    }

    return JsonResponse(response_data)
