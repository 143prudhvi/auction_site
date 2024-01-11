from django.shortcuts import render
from .models import Item
import os, json
from django.db.models import Min
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core import serializers
# from django.core.paginator import Paginator

def filtered_items(request):
    brand = request.GET.get('brand', None)
    seller = request.GET.get('seller', None)
    search_id = request.GET.get('search_id', None)
    
    # # Pagination 
    # page = request.GET.get('page' ,1)
    # size = request.GET.get('size', 24)
    
    # Retriving first item 
    items = Item.objects.values('itemId').annotate(first_item_id=Min('id'))
    items = Item.objects.filter(id__in=items.values('first_item_id'))

    # Filtering
    if search_id:
        items = items.filter(itemId=search_id)
        
    if brand:
        items = items.filter(brand=brand)
    
    if seller:
        items = items.filter(sellerName=seller)
    
    # # Pagination
    # p = Paginator(items, size)
    # items = p.get_page(page)
    items = items[:36]
    # Images and Description
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
        'item_descriptions': item_descriptions,
        'search_id' : search_id if search_id else ""
    }

    return render(request, 'filtered_items.html', context)

def get_images_from_path(folder_path : str):
    file_list = [folder_path + "/" + f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return file_list

def load_items(request):
    offset = int(request.GET.get('offset', 0))
    brand = request.GET.get('brand', None)
    seller = request.GET.get('seller', None)
    search_id = request.GET.get('search_id', None)
    
    # Retriving first item 
    items = Item.objects.values('itemId').annotate(first_item_id=Min('id'))
    items = Item.objects.filter(id__in=items.values('first_item_id'))

    # Filtering
    if search_id:
        items = items.filter(itemId=search_id)
        
    if brand:
        items = items.filter(brand=brand)
    
    if seller:
        items = items.filter(sellerName=seller)

    items = items[offset:offset+24]
    
    item_images = {}
    item_descriptions = {}
    for item in items:
        item_images[item.itemId] = get_images_from_path("static/Images/" + item.itemId)
        # item_descriptions[item.itemId] = [feature for feature in item.itemDescription.split("\n") if feature]
    distinct_brands = Item.objects.values_list('brand', flat=True).order_by('brand').distinct()
    distinct_sellers = Item.objects.values_list('sellerName', flat=True).order_by('sellerName').distinct()
    serialized_data = serializers.serialize("json", items)
    serialized_data = json.loads(serialized_data)
    serialized_data 
    context = {
        'items': serialized_data,
        'item_images': item_images,
        'item_descriptions': item_descriptions
    }
    # html = render_to_string('items_list.html', context)
    return JsonResponse(context)