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
from django.http import JsonResponse


@method_decorator(login_required, name='dispatch')
class AddToCartView(APIView):
    serializer_class = CartItemSerializer  # Define the serializer class

    def post(self, request, product_id):  # Include 'self' here
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
