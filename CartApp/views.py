from audioop import reverse

from django.conf import settings
import requests
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from CartApp.cart import Cart
from CartApp.models import CartModel


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
        cart_count = cart.count()
        response = {
            'cart_count': cart_count,
            'status': True
        }
        return JsonResponse(response)
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
    html = render(request, 'partials/cart-partial.html', {'cart': cart})
    response = {
        'html': html.content.decode('utf-8'),
        'cart_count': '0'
    }
    return JsonResponse(response)


def remove_product(request):
    product_id = request.GET.get('product_id')
    color_id = request.GET.get('color_id')
    cart = Cart(request)
    cart.remove(product_id, color_id, request.user)
    html = render(request, 'partials/price-partial.html', {'cart': cart})
    response = {
        'html': html.content.decode('utf-8'),
        'cart_count': cart.count()
    }
    return JsonResponse(response)


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
    cart_count = cart.count()
    response = {
        'off_price': off_price,
        'final_price': final_price,
        'html': html.content.decode('utf-8'),
        'cart_count': cart_count
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


# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/verify/'

# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "برای ثبت سفارش ابتدا مبلغ را پرداخت کنید."  # Required
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/verify/'

def send_request(request):
    cart = Cart(request)
    amount = cart.get_payable_price() * 10
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Description": description,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        if response.status_code == 200:
            response_data = response.json()  # استفاده از یک نام متغیر جدید برای داده‌های JSON
            if response_data['Status'] == 100:
                return redirect(ZP_API_STARTPAY + response_data['Authority'])
            else:
                return JsonResponse({'status': False, 'code': str(response_data['Status'])})
        return JsonResponse({'status': False, 'code': str(response.status_code)})
    except requests.exceptions.Timeout:
        return JsonResponse({'status': False, 'code': 'timeout'})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': False, 'code': 'connection error'})


def verify(request):
    authority = request.GET['Authority']
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data['Status'] == 100:
            cart_model = CartModel.objects.filter(user=request.user, status='در انتظار پرداخت').first()
            cart_model.status = 'پرداخت شده'
            cart_model.save()
            cart = Cart(request)
            cart.clear(request.user)
            return render(request, 'cart_app/cart.html', {'cart': cart})
        else:
            return JsonResponse({'status': False, 'code': str(response_data['Status'])})
    return redirect('CartApp:cart')
