from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartItemSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly



@api_view(['POST'])
@permission_classes([IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly])
def add_to_cart(request):
    user = request.user
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    product = get_object_or_404(Product, id=product_id)
    print(user)
    print(product)

    if not user.is_authenticated:
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    # Get the user's cart or create one if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=user)

    # Add the product to the cart
    cart.add_product(product, quantity=quantity)

    # Serialize the CartItem and return it in the response
    cart_item = CartItem.objects.get(cart=cart, product=product)
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)