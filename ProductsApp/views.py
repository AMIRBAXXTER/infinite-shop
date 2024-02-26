from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse
from IndexApp.models import SiteInfo
from .models import *


# Create your views here.
def product_detail(request: HttpRequest, product_id):
    product: Product = Product.objects.select_related('brand').prefetch_related('category',
                                                                                'rate',
                                                                                'comment').filter(
        id=product_id).first()
    avg = int(product.average_rate)
    blank_star = 5 - avg
    main_category = product.category.filter(parent=None).first()
    product_comments = ProductComment.objects.filter(product=product, parent=None)
    product_all_comments = ProductComment.objects.filter(product=product)
    product_color = ProductColor.objects.filter(product=product).first()
    product_properties = ProductProperty.objects.filter(product=product)
    context = {
        'product': product,
        'star_range': range(1, (avg + 1)),
        'blank_star': range(1, (blank_star + 1)),
        'main_category': main_category,
        'product_comments': product_comments,
        'product_all_comments': product_all_comments,
        'product_color': product_color,
        'product_properties': product_properties,

    }
    return render(request, 'products_app/product_detail.html', context)


def product_list(request: HttpRequest):
    products = Product.objects.filter(is_active=True).all()
    site_info = SiteInfo.objects.filter(is_active=True).first()
    main_category = Category.objects.filter(parent=None).all()


    context = {
        'products': products,
        'site_info': site_info,
        'main_category': main_category,
    }
    return render(request, 'products_app/product_list.html', context)
