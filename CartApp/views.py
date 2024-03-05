from django.http import JsonResponse
from django.shortcuts import render
from CartApp.cart import Cart


# Create your views here.

def add_to_cart(request):
    try:
        product_id = request.GET.get('product_id')
        product_color_id = request.GET.get('color_id')
        if not product_color_id:
            return JsonResponse({'status': "color_id"})
        count = request.GET.get('count')
        cart = Cart(request)
        cart.add(product_id, product_color_id, count)
        return JsonResponse({'status': True})
    except:
        return JsonResponse({'status': False})


def cart(request):
    cart = Cart(request)
    return render(request, 'cart_app/cart.html', {'cart': cart})


def cart_products(request):
    cart = Cart(request)
    return render(request, 'partials/cart-partial.html', {'cart': cart})


def empty_cart(request):
    cart = Cart(request)
    cart = cart.clear()
    return render(request, 'partials/cart-partial.html', {'cart': cart})


def remove_product(request):
    product_id = request.GET.get('product_id')
    color_id = request.GET.get('color_id')
    cart = Cart(request)
    cart.remove(product_id, color_id)
    return render(request, 'partials/price-partial.html', {'cart': cart})
