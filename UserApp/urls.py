from django.urls import path

from UserApp import views

app_name = 'UserApp'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
]