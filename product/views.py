from django.shortcuts import render
from .models import Item, MatchItems
import os, json
from django.db.models import Min
from django.http import JsonResponse
from django.core import serializers
import uuid

def filtered_items(request):
    brand = request.GET.get('brand', "kate spade")
    seller = request.GET.get('seller', "AllSeasons")
    search_id = request.GET.get('search_id', None)
    title_search = request.GET.get('title_search', None)
    platform = request.GET.get('platform', "Poshmark")
    image_exist = request.GET.get('image_exist', None)
    duplicate_group = request.GET.get('duplicate_group', None)
    is_new_image = request.GET.get('is_new_image', None)
    is_new_group = request.GET.get('is_new_group', None)
    
    
    
    # Get all items with their corresponding minimum id
    items_with_min_ids = Item.objects.values('itemId').annotate(first_item_id=Min('id'))

    # Filter items to include only those with minimum ids
    items = Item.objects.filter(id__in=items_with_min_ids.values('first_item_id'))
        
    # Filtering
    if title_search:
        items = items.filter(title__icontains=title_search)
    
    if search_id:
        items = items.filter(itemId__in=search_id.split(","))
        
    if brand:
        items = items.filter(brand=brand)
    
    if seller:
        items = items.filter(sellerName=seller)
    
    if platform:
        items = items.filter(platform=platform)
    
    if image_exist:
        items = items.filter(imageExist=True)
        
    if is_new_image:
        items = items.filter(isNewImage=True)
        
    if is_new_group:
        items = items.filter(isNewGroup=True)
    
    if duplicate_group:
        unique_group_ids = items.values('groupId').annotate(first_group_id=Min('id'))
        items_with_unique_groups = items.filter(id__in=unique_group_ids.values('first_group_id'))
        items_with_null_group_ids = items.filter(groupId__isnull=True)
        items = items_with_unique_groups | items_with_null_group_ids
    
    total_items = len(items)
    
    # items = items[:36]
    # Images and Description
    item_images = {}
    item_descriptions = {}
    for item in items:
        item_images[item.itemId] = get_images_from_path("static/Images/" + item.itemId, item.imageExist)
        # item_descriptions[item.itemId] = [feature for feature in item.itemDescription.split("\n") if feature]
    distinct_brands = Item.objects.filter(platform=platform, sellerName=seller).values_list('brand', flat=True).order_by('brand').distinct()
    distinct_sellers = Item.objects.values_list('sellerName', flat=True).order_by('sellerName').distinct()
    
    context = {
        'items': items,
        'distinct_brands': distinct_brands,
        'distinct_sellers': distinct_sellers,
        'selected_platform' : platform if platform else "",
        'selected_brand': brand if brand else "",
        'selected_seller': seller if seller else "",
        'item_images': item_images,
        'item_descriptions': item_descriptions,
        'search_id' : search_id if search_id else "",
        'title_search' : title_search if title_search else "",
        'image_exist' : True if image_exist else False,
        'duplicate_group' : True if duplicate_group else False,
        'is_new_image' : True if is_new_image else False,
        'is_new_group' : True if is_new_group else False,
        'total_items' : total_items
    }

    return render(request, 'filtered_items.html', context)

def get_images_from_path(folder_path : str, imageExist: bool):
    if not imageExist or not os.path.exists(folder_path):
        folder_path = "static/Images/dummy"
        
    file_list = ["/" + folder_path + "/" + f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return file_list

# def load_items(request):
#     offset = int(request.GET.get('offset', 0))
#     brand = request.GET.get('brand', None)
#     seller = request.GET.get('seller', None)
#     search_id = request.GET.get('search_id', None)
#     title_search = request.GET.get('title_search', None)
#     platform = request.GET.get('platform', None)
#     image_exist = request.GET.get('image_exist', None)
#     duplicate_group = request.GET.get('duplicate_group', None)

#     # Retriving first item 
#     items = Item.objects.values('itemId').annotate(first_item_id=Min('id'))
#     items = Item.objects.filter(id__in=items.values('first_item_id'))
#     if duplicate_group:
#         unique_group_ids = items.values('groupId').annotate(first_group_id=Min('id'))
#         items_with_unique_groups = items.filter(id__in=unique_group_ids.values('first_group_id'))
#         items_with_null_group_ids = items.filter(groupId__isnull=True)
#         items = items_with_unique_groups | items_with_null_group_ids
#     # Filtering
#     if title_search:
#         items = items.filter(title__icontains=title_search)
        
#     if search_id:
#         items = items.filter(itemId__in=search_id.split(","))
        
#     if brand:
#         items = items.filter(brand=brand)
    
#     if seller:
#         items = items.filter(sellerName=seller)
    
#     if platform:
#         items = items.filter(platform=platform)
    
#     if image_exist:
#         items = items.filter(imageExist=True)

#     items = items[offset:offset+24]
    
#     item_images = {}
#     item_descriptions = {}
#     for item in items:
#         item_images[item.itemId] = get_images_from_path("static/Images/" + item.itemId)
#     serialized_data = serializers.serialize("json", items)
#     serialized_data = json.loads(serialized_data)
#     serialized_data 
#     context = {
#         'items': serialized_data,
#         'item_images': item_images,
#         'item_descriptions': item_descriptions
#     }
#     # html = render_to_string('items_list.html', context)
#     return JsonResponse(context)

def saveMatchedItems(request):
    itemId = request.GET.get('itemId')
    matchedId : str = request.GET.get('matchedId')
    matchedItems = MatchItems.objects.filter(itemId=itemId)
    retrivedMatchedIds = [obj.matchedId for obj in matchedItems ]
    matchedIdsList = matchedId.split(",")
    matchedIdsListCopy = matchedIdsList.copy()
    if matchedId:  
        for id in matchedIdsListCopy:
            if id not in retrivedMatchedIds:
                MatchItems.objects.create(itemId=itemId, matchedId=id)
                MatchItems.objects.create(itemId=id, matchedId=itemId)
                updateMatchedItemCount(itemId=itemId,matchedId=id, count=1)
            else:
                matchedIdsList.remove(id)
                retrivedMatchedIds.remove(id)
        for id in retrivedMatchedIds:
            MatchItems.objects.filter(itemId=itemId, matchedId=id).delete()
            MatchItems.objects.filter(itemId=id, matchedId=itemId).delete()
            updateMatchedItemCount(itemId=itemId,matchedId=id, count=-1)
        updateisMatched(idsList=matchedIdsListCopy + [itemId])
        return JsonResponse({
            "status" : "success",
            "message" : "Saved matched Items Successfully"
        })
    else:
        for id in retrivedMatchedIds:
            MatchItems.objects.filter(itemId=itemId, matchedId=id).delete()
            MatchItems.objects.filter(itemId=id, matchedId=itemId).delete()
            updateMatchedItemCount(itemId=itemId,matchedId=id, count=-1)
        updateisMatched(idsList=matchedIdsListCopy + [itemId])
        return JsonResponse({
            "status" : "success",
            "message" : "Cleared Matching Successfully"
        })
    
        
def getMatchedItems(request):
    itemId = request.GET.get('itemId')
    items = MatchItems.objects.filter(itemId=itemId)
    if items.exists():     
        retrivedMatchedIds = [obj.matchedId for obj in items ]
        return JsonResponse({
            "status" : "success",
            "numberOfRecords" : len(retrivedMatchedIds),
            "message" : "Retrived matched Ids Successfully",
            "matchedIds" : ",".join(retrivedMatchedIds)
        })
    else:
        return JsonResponse({
            "status" : "success",
            "numberOfRecords" : 0,
            "message" : "No matched Items found for Id " + itemId
        })

def updateMatchedItemCount(itemId, matchedId, count):
        items = Item.objects.filter(itemId=itemId)
        items.update(matchedCount=items[0].matchedCount + count)
        
        matchedItems = Item.objects.filter(itemId=matchedId)
        matchedItems.update(matchedCount=matchedItems[0].matchedCount + count)

def updateisMatched(idsList : list):
    for id in idsList:
        items = MatchItems.objects.filter(itemId=id)
        if len(items):
            Item.objects.filter(itemId=id).update(isMatched=1)
        else:
            Item.objects.filter(itemId=id).update(isMatched=0)

def groupItems(request):
    groupedIds = request.GET.get('groupedIds')
    nonGroupedIds = request.GET.get('nonGroupedIds')
    
    groupedIdList = groupedIds.split(",")
    nonGroupedIdList = nonGroupedIds.split(",")
    
    if(not groupedIds):
        groupId = uuid.uuid4()
        for itemId in nonGroupedIdList:
            Item.objects.filter(itemId=itemId).update(isGrouped=1,groupId=groupId)
    else:
        items = Item.objects.filter(itemId=groupedIdList[0])
        groupId = items[0].groupId
        if(len(groupedIdList) > 1):
            for itemId in groupedIdList[1:]:
                Item.objects.filter(itemId=itemId).update(groupId=groupId)
        for itemId in nonGroupedIdList:
            Item.objects.filter(itemId=itemId).update(isGrouped=1,groupId=groupId)
    return JsonResponse({
            "status" : "success",
            "message" : "Grouped Items Successfully!!"
        })
    
def removeGroupItems(request):
    itemIds = request.GET.get('itemIds')
    for itemId in itemIds.split(","):
        Item.objects.filter(itemId=itemId).update(isGrouped=0,groupId=None)
    return JsonResponse({
            "status" : "success",
            "message" : "Removed Items Successfully from Group!!"
        })

def addGroupItem(request):
    itemId = request.GET.get('itemId')
    groupId = request.GET.get('groupId')
    
    items = Item.objects.filter(itemId=itemId)
    if len(items):
        items.update(groupId=groupId)
        return JsonResponse({
            "status" : "success",
            "message" : "Added Item Successfully to the Group!!"
        })
    else:
        return JsonResponse({
            "status" : "error",
            "message" : "No Item found with Id : " + itemId
        })

def get_group_page(request, id):
    
    # Retriving first item 
    items = Item.objects.values('itemId').annotate(first_item_id=Min('id'))
    items = Item.objects.filter(id__in=items.values('first_item_id'))

    items = items.filter(groupId=id)
    
    # Images and Description
    item_images = {}
    for item in items:
        item_images[item.itemId] = get_images_from_path("static/Images/" + item.itemId, item.imageExist)
    
    context = {
        'items': items,
        'item_images': item_images,
        'group_id' : id
    }

    return render(request, 'group_page.html', context)

def get_brand_list(request):
    seller = request.GET.get('seller')
    platform = request.GET.get('platform')
    distinct_brands = Item.objects.filter(platform=platform, sellerName=seller).values_list('brand', flat=True).order_by('brand').distinct()
    brands = []
    for item in distinct_brands:
        brands.append(item)
        
    return JsonResponse({
            "status" : "success",
            "brands" : brands
        })