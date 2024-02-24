from django.shortcuts import render

from .models import Product


# Create your views here.
def product_detail(request, product_id):
    product: Product = Product.objects.filter(id=product_id).first()
    avg = int(product.average_rate)
    blank_star = 5 - avg
    context = {
        'product': product,
        'star_range': range(1, (avg + 1)),
        'blank_star': range(1, (blank_star + 1)),

    }
    return render(request, 'products_app/product_detail.html', context)
