from django.utils.text import slugify
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommshell.settings')
import django
import random
import string

django.setup()

from products.models import Product

# Define the list of possible titles for the products
titles = ["Product " + str(i+1) for i in range(100)]

# Generate 100 instances of the Product model
for title in titles:
    # Create a new product instance
    product = Product()
    # Set the title
    product.title = title
    # Set the slug
    slug = slugify(product.title)
    count = 1
    while Product.objects.filter(slug=slug).exists():
        count += 1
        slug = f"{slugify(product.title)}-{count}"
    product.slug = slug
    # Set the description
    product.description = "This is the description for " + title
    # Set the regular price
    product.regular_price = random.randint(10, 50)
    # Set the discount price (50% chance of having a discount price)
    if random.random() < 0.5:
        product.discount_price = random.randint(5, product.regular_price)
    # Set the amount
    product.amount = random.randint(1, 10)
    # Save the product instance to the database
    product.save()
