from django.urls import path

from UserApp import views
from django.contrib.auth import views as auth_views

app_name = 'UserApp'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url='/password-reset/complete'),
         name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('profile/', views.user_profile, name='profile'),
    path('favorite-products/', views.favorite_products, name='favorite_products'),
    path('addresses/', views.addresses, name='addresses'),
    path('factors/', views.factors, name='factors'),
    path('get-city/', views.get_city, name='get_city'),
    path('add-address/', views.add_address, name='add_address'),
    path('delete-address/', views.delete_address, name='delete_address'),
    path('activate-address/', views.activate_address, name='activate_address'),
    path('edit-address/', views.edit_address, name='edit_address')
]
