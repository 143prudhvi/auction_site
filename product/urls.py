from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.filtered_products, name='filtered_products'),
]
urlpatterns += staticfiles_urlpatterns()