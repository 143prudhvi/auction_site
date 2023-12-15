from django.shortcuts import render
from .models import Item
import os
from django.db.models import Min

def filtered_items(request):
    brand = request.GET.get('brand', None)
    seller = request.GET.get('seller', None)
    items = Item.objects.values('itemId').annotate(first_item_id=Min('id'))
    items = Item.objects.filter(id__in=items.values('first_item_id'))

    print(len(items))
    if brand:
        items = items.filter(brand=brand)
    
    if seller:
        items = items.filter(sellerName=seller)
    
    items = items[:100]
    item_images = {}
    item_descriptions = {}
    for item in items:
        item_images[item.itemId] = get_images_from_path("static/Images/" + item.itemId)
        # item_descriptions[item.itemId] = [feature for feature in item.itemDescription.split("\n") if feature]
    distinct_brands = Item.objects.values_list('brand', flat=True).order_by('brand').distinct()
    distinct_sellers = Item.objects.values_list('sellerName', flat=True).order_by('sellerName').distinct()
    
    context = {
        'items': items,
        'distinct_brands': distinct_brands,
        'distinct_sellers': distinct_sellers,
        'selected_brand': brand,
        'selected_seller': seller ,
        'item_images': item_images,
        'item_descriptions': item_descriptions
    }

    return render(request, 'filtered_items.html', context)

def get_images_from_path(folder_path : str):
    file_list = [folder_path + "/" + f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return file_list
