from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def add_product(self, product, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product
        )
        if not created:  # Only increment the quantity if the cart item already exists
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

    def remove_product(self, product):
        CartItem.objects.filter(cart=self, product=product).delete()

    def calculate_total(self):
        total = 0
        for item in self.items.all():
            total += item.product.regular_price * item.quantity
        return total

    @property
    def items(self):
        return CartItem.objects.filter(cart=self)
