import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommshell.settings')
django.setup()

from django.core.files import File
from products.models import Product, ProductImage

titles = ["Product " + str(i+1) for i in range(100)]

image_dir = 'media/images'

for i, title in enumerate(titles):
    product, created = Product.objects.get_or_create(title=title)

    # Check if product already has an image associated with it
    existing_images = ProductImage.objects.filter(product=product)

    if existing_images.exists():
        print(f"Product {product.title} already has an image, skipping.")
    else:
        # Create a ProductImage instance for each product
        product_image = ProductImage()
        product_image.product = product
        product_image.alt_text = f'Image for {product.title}'

        # Set the image. The image filename cycles through the 16 available images.
        image_filename = f'image{(i % 16) + 1}.png'
        image_path = os.path.join(image_dir, image_filename)
        try:
            with open(image_path, 'rb') as img_file:
                product_image.image.save(
                    image_filename, File(img_file), save=True)
        except Exception as e:
            print(f"Unable to add image for product {product.title}: {e}")
