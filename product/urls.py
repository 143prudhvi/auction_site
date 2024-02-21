from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.filtered_items, name='filtered_items'),
    path('load_more_items', views.load_items, name='load_more_items'),
    path('saveMatchedItems', views.saveMatchedItems, name='save_matched_items'),
    path('getMatchedIds', views.getMatchedItems, name='get_matched_ids'),
    path('groupItems', views.groupItems, name="group_items"),
    path('removeGroupItems', views.removeGroupItems, name="remove_group_items"),
    path("group/<str:id>/", views.get_group_page, name="get_group_page"),
    path('addGroupItem', views.addGroupItem, name='add_group_item'),
    
]
urlpatterns += staticfiles_urlpatterns()