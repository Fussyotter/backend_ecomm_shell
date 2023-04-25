from django.db import models
from django.contrib.auth.models import User
from cart.models import Cart
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    products = models.ManyToManyField('Product', through='OrderProduct')
