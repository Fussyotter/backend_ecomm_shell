from django.db import models
from django.urls import reverse
from django.utils.timezone import now
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
    """
    Product Model
    """
    product_type = models.ForeignKey(
        ProductType, on_delete=models.RESTRICT, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, null=True)
    title = models.CharField(verbose_name=_("title"),help_text=("required"),max_length=255, null=True)
    description = models.TextField(verbose_name=_("description"),help_text=("not required"), blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True)
    regular_price = models.DecimalField(verbose_name=_(
        "regular price"), max_digits=5, decimal_places=2, default=0)
    discount_price = models.DecimalField(verbose_name=_(
        "discount price"), max_digits=5, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(verbose_name=_("Product visibility"),help_text=_("change product visibility"),default=True)
    created_at = models.DateTimeField(verbose_name=_("created at"), default=now)
    updated_at = models.DateTimeField(verbose_name=_("updated at"), default=now)
    amount = models.IntegerField(verbose_name=_(
        "amount"), default=0, editable=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_absolute_url(self):
        """
        Return absolute url
        """
        return reverse("products:product_detail", args=[self.slug])
    def __str__(self):  
        return self.title
    
class ProductSpecificationValue(models.Model):
    """ 
    Product Specification Value Model
    
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(verbose_name=_("Value"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")
       

    def __str__(self):
        return self.value
    
class ProductImage(models.Model):
    """
    Product Image Model
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(verbose_name=_("image"),help_text=_("Upload a product image"), upload_to="images/", default="images/default.png", null=True, blank=True)
    alt_text = models.CharField(verbose_name=_("alt text"),help_text=_("Enter alt text for image"), max_length=255, null=True, blank=True)
    is_feature = models.BooleanField(verbose_name=_("feature image"),help_text=_("feature image"), default=False)
    created_at = models.DateTimeField(verbose_name=_("created at"), default=now)
    updated_at = models.DateTimeField(verbose_name=_("updated at"), default=now)        

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return self.product.title