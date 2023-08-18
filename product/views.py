from django.shortcuts import render
from .models import Product

def filtered_products(request):
    brand = request.GET.get('brand', None)
    seller = request.GET.get('seller', None)

    products = Product.objects.all()

    if brand:
        products = products.filter(brand=brand)
    
    if seller:
        products = products.filter(sellerName=seller)
    
    distinct_brands = Product.objects.values_list('brand', flat=True).distinct()
    distinct_sellers = Product.objects.values_list('sellerName', flat=True).distinct()
    
    context = {
        'products': products,
        'distinct_brands': distinct_brands,
        'distinct_sellers': distinct_sellers,
        'selected_brand': brand,
        'selected_seller': seller 
    }

    return render(request, 'filtered_products.html', context)
