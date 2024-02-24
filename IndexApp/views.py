from django.shortcuts import render

from IndexApp.models import *
from ProductsApp.models import Product


# Create your views here.

def index(request):
    return render(request, 'index_app/index.html')


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
