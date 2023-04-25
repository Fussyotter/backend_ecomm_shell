from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    carts = models.ManyToManyField('cart.Cart')
    orders = models.ManyToManyField(
        'orders.Order', related_name='products', through='orders.OrderProduct')

    def __str__(self):
        return self.name
