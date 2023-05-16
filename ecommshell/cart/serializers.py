from rest_framework import serializers
from .models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity')
        read_only_fields = ('id', 'cart')

        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'created_at')
        read_only_fields = ('id', 'user', 'items', 'created_at')