from django.urls import path

from IndexApp import views

app_name = 'IndexApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.about_us, name='about_us'),
    path('search/', views.search, name='search'),
]