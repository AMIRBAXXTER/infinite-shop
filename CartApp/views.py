from django.contrib.auth.decorators import login_required
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
        cart.add(product_id, product_color_id, count, user=request.user)
        return JsonResponse({'status': True})
    except:
        return JsonResponse({'status': False})


def cart(request):
    cart = Cart(request)
    for item in cart.__iter__(include_product=False):
        cart.add(item['id'], item['color_id'], user=request.user)
    return render(request, 'cart_app/cart.html', {'cart': cart})


def cart_products(request):
    cart = Cart(request)
    return render(request, 'partials/cart-partial.html', {'cart': cart})


def cart_prices(request):
    cart = Cart(request)
    return render(request, 'partials/price-partial.html', {'cart': cart})


def empty_cart(request):
    cart = Cart(request)
    cart = cart.clear(request.user)
    return render(request, 'partials/cart-partial.html', {'cart': cart})


def remove_product(request):
    product_id = request.GET.get('product_id')
    color_id = request.GET.get('color_id')
    cart = Cart(request)
    cart.remove(product_id, color_id, request.user)
    return render(request, 'partials/price-partial.html', {'cart': cart})


def update_count(request):
    update_type = request.GET.get('type')
    product_id = request.GET.get('product_id')
    color_id = request.GET.get('color_id')
    cart = Cart(request)
    if update_type == 'increase':
        cart.increase(product_id, color_id, request.user)
    elif update_type == 'decrease':
        cart.decrease(product_id, color_id, request.user)
    html = render(request, 'partials/price-partial.html', {'cart': cart})
    off_price = cart.get_off_price(product_id, color_id)
    final_price = cart.get_final_price(product_id, color_id)
    response = {
        'off_price': off_price,
        'final_price': final_price,
        'html': html.content.decode('utf-8')
    }
    return JsonResponse(response)

@login_required
def checkout(request):
    cart = Cart(request)
    active_address = request.user.addresses.filter(is_active=True).first()
    context = {
        'cart': cart,
        'active_address': active_address
    }
    return render(request, 'cart_app/checkout.html', context)
