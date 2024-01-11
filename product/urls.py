from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.filtered_items, name='filtered_items'),
    path('load_more_items', views.load_items, name='load_more_items'),
    
]
urlpatterns += staticfiles_urlpatterns()