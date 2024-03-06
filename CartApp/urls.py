from django.urls import path

from CartApp import views

app_name = 'CartApp'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-product/', views.remove_product, name='remove_product'),
    path('empty-cart/', views.empty_cart, name='empty_cart'),
    path('update-count/', views.update_count, name='update_count'),
]