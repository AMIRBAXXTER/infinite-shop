from django.urls import path

from ProductsApp import views

app_name = 'ProductsApp'

urlpatterns = [
    path('product-detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product-list/', views.ProductListView.as_view(), name='product_list'),
    path('product-list/category/<str:category>/', views.ProductListView.as_view(), name='products_by_category'),
    path('product-list/brand/<str:brand>/', views.ProductListView.as_view(), name='products_by_brand'),
    path('product-color-stock/', views.color_stock, name='product_color_stock'),
    path('add-comment/', views.product_comment, name='product_comment'),
    path('delete-comment/', views.delete_comment, name='delete_comment'),
    path('add-favorite/', views.add_product_to_favorite, name='add_product_to_favorite'),
    path('add-rate/', views.add_rate, name='add_rate'),
]