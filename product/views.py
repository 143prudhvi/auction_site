from django.shortcuts import render
from .models import Product
import os

def filtered_products(request):
    brand = request.GET.get('brand', None)
    seller = request.GET.get('seller', None)
    products = Product.objects.all()

    if brand:
        products = products.filter(brand=brand)
    
    if seller:
        products = products.filter(sellerName=seller)
    product_images = {}
    product_descriptions = {}
    for product in products:
        product_images[product.productId] = get_images_from_path("static/Images/" + product.pictureLocation)
        product_descriptions[product.productId] = [feature for feature in product.productDescription.split("\n") if feature]
    distinct_brands = Product.objects.values_list('brand', flat=True).order_by('brand').distinct()
    distinct_sellers = Product.objects.values_list('sellerName', flat=True).order_by('sellerName').distinct()
    
    context = {
        'products': products,
        'distinct_brands': distinct_brands,
        'distinct_sellers': distinct_sellers,
        'selected_brand': brand,
        'selected_seller': seller ,
        'product_images': product_images,
        'product_descriptions': product_descriptions
    }

    return render(request, 'filtered_products.html', context)

def get_images_from_path(folder_path : str):
    file_list = [folder_path + f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return file_list
