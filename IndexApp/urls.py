from django.urls import path

from IndexApp import views

app_name = 'IndexApp'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('about-us/', views.AboutUs.as_view(), name='about_us'),
    path('search/', views.Search.as_view(), name='search'),
]