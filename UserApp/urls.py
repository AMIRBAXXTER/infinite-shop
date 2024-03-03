from django.urls import path

from UserApp import views

app_name = 'UserApp'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('favorite-products/', views.favorite_products, name='favorite_products'),
    path('addresses/', views.addresses, name='addresses'),
    path('get-city/', views.get_city, name='get_city'),
    path('add-address/', views.add_address, name='add_address'),
    path('delete-address/', views.delete_address, name='delete_address'),
    path('activate-address/', views.activate_address, name='activate_address'),
    path('edit-address/', views.edit_address, name='edit_address')
]
