from django.db.models import Count
from django.shortcuts import render

from IndexApp.models import *
from ProductsApp.models import Product


# Create your views here.

def index(request):
    site_info = SiteInfo.objects.filter(is_active=True).first()
    main_pictures = MainPictures.objects.filter(site_info=site_info).all()
    side_pictures = SidePicture.objects.filter(site_info=site_info).all()
    featured_products = Product.objects.filter(is_active=True).order_by('-average_rate')[:4]
    off_products = Product.objects.filter(is_active=True).order_by('-off_percent')[:4]
    most_viewed_products = Product.objects.annotate(num_visits=Count('product_visited')).order_by('-num_visits')[:4]
    context = {
        'main_pictures': main_pictures,
        'side_pictures': side_pictures,
        'featured_products': featured_products,
        'off_products': off_products,
        'most_viewed_products': most_viewed_products,

    }
    return render(request, 'index_app/index.html', context)


def about_us(request):
    site_info = SiteInfo.objects.filter(is_active=True).first()
    team_members = TeamMember.objects.filter(site_info=site_info)
    context = {
        'site_info': site_info,
        'team_members': team_members
    }
    return render(request, 'index_app/about_us.html', context)


def header(request):
    site_info: SiteInfo = SiteInfo.objects.filter(is_active=True).first()
    context = {
        'site_info': site_info
    }
    return render(request, 'infinite shop/partial/header.html', context)


def footer(request):
    site_info: SiteInfo = SiteInfo.objects.filter(is_active=True).first()
    context = {
        'site_info': site_info
    }
    return render(request, 'infinite shop/partial/footer.html', context)
