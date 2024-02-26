from django.urls import path

from ProductsApp import views

app_name = 'ProductsApp'

urlpatterns = [
    path('product-detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product-list/', views.product_list, name='product_list'),
]