from rest_framework import serializers
from products.serializers import ProductSerializer
from .models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity')
        read_only_fields = ('id', 'cart')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'total', 'created_at')
        read_only_fields = ('id', 'user', 'items', 'total', 'created_at')

    def get_total(self, obj):
        return obj.calculate_total()
