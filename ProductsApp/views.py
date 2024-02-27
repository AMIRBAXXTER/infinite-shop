from django.contrib.auth.decorators import login_required
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
    product_comments = ProductComment.objects.filter(product=product, parent=None).order_by('-created_at')
    product_all_comments = ProductComment.objects.filter(product=product)
    product_color = ProductColor.objects.filter(product=product).first()
    product_properties = ProductProperty.objects.filter(product=product)
    related_products = Product.objects.filter(category__in=product.category.all()).order_by('-created_at').exclude(
        id=product.id)
    print(related_products)
    context = {
        'product': product,
        'star_range': range(1, (avg + 1)),
        'blank_star': range(1, (blank_star + 1)),
        'main_category': main_category,
        'product_comments': product_comments,
        'product_all_comments': product_all_comments,
        'product_color': product_color,
        'product_properties': product_properties,
        'related_products': related_products,

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


def color_stock(request: HttpRequest):
    product_id = request.GET.get('product_id')
    product_color = request.GET.get('product_color')
    product = Product.objects.filter(id=product_id).first()
    stock = ProductColor.objects.filter(product=product, color=product_color).first()
    response = {
        'stock': stock.stock,
        'title': stock.title,
        'color': stock.color,
    }
    return JsonResponse(response)


@login_required
def product_comment(request: HttpRequest):
    product_id = request.GET.get('product_id')
    product = Product.objects.filter(id=product_id).first()
    comment = request.GET.get('comment')
    user = request.user
    parent_id = request.GET.get('parent')
    parent = ProductComment.objects.filter(id=parent_id).first() if parent_id else None
    new_comment = ProductComment(product=product, user=user, comment=comment, parent=parent)
    new_comment.save()
    comments = ProductComment.objects.filter(product=product, parent=None).order_by('-created_at')

    context = {
        'product_comments': comments
    }
    return render(request, 'partials/comments_partial.html', context)

