from django.urls import path

from CartApp import views

app_name = 'CartApp'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/', views.AddToCart.as_view(), name='add_to_cart'),
    path('remove-product/', views.RemoveProduct.as_view(), name='remove_product'),
    path('empty-cart/', views.EmptyCart.as_view(), name='empty_cart'),
    path('update-count/', views.UpdateCount.as_view(), name='update_count'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('request/', views.SendRequest.as_view(), name='request'),
    path('verify/', views.Verify.as_view(), name='verify'),
]
