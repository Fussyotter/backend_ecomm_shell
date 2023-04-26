from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    """
    Category Model
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)

    class MPPTMeta:
        order_insertion_by = ['name']
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        """
        Return absolute url
        """
        return reverse('products:category_list', args=[self.slug])
    def __str__(self):
        return self.name
    
class ProductType(models.Model):
    """ 
    Product Type Model
    
    """
    name = models.CharField(verbose_name=_("Product Name"),help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name
    
class ProductSpecification(models.Model):
    """ 
    Product Specification Model
    
    """
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")
        ordering = ("product_type", "name")

    def __str__(self):
        return self.name








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
