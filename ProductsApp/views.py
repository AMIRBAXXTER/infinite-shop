from django.http import HttpRequest
from django.shortcuts import render

from .models import *


# Create your views here.
def product_detail(request: HttpRequest, product_id):
    product: Product = Product.objects.filter(id=product_id).first()
    avg = int(product.average_rate)
    blank_star = 5 - avg
    main_category = product.category.filter(parent=None).first()
    product_comments = ProductComment.objects.filter(product=product, parent=None)
    context = {
        'product': product,
        'star_range': range(1, (avg + 1)),
        'blank_star': range(1, (blank_star + 1)),
        'main_category': main_category,
        'product_comments': product_comments

    }
    return render(request, 'products_app/product_detail.html', context)
