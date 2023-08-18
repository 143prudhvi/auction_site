from django.urls import path
from . import views

urlpatterns = [
    path('', views.filtered_products, name='filtered_products'),
]
