from django.urls import path

from ProductsApp import views

app_name = 'ProductsApp'

urlpatterns = [
    path('product-detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product-list/', views.ProductListView.as_view(), name='product_list'),
    path('product-list/order-by/<str:order_by>', views.ProductListView.as_view(), name='order_by'),
    path('product-color-stock/', views.color_stock, name='product_color_stock'),
    path('add-comment/', views.product_comment, name='product_comment'),
]