from products.models import Product, ProductImage
from django.core.files import File

titles = ["Product " + str(i+1) for i in range(100)]

image_dir = 'media/images'

for i, title in enumerate(titles):
    product = Product()
    product.title = title

    product.save()

    # Create a ProductImage instance for each product
    product_image = ProductImage()
    product_image.product = product
    product_image.alt_text = f'Image for {product.title}'

    # Set the image
    image_filename = f'image{i+1}.jpg'
    image_path = os.path.join(image_dir, image_filename)
    with open(image_path, 'rb') as img_file:
        product_image.image.save(image_filename, File(img_file), save=True)
# need to add images to media/images that fit the above code