from django.conf import settings
import requests
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from CartApp.cart import Cart
from CartApp.models import CartModel


# Create your views here.

class AddToCart(View):
    def get(self, request):
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


class CartView(View):
    template_name = 'cart_app/cart.html'

    def get(self, request):
        cart = Cart(request)
        for item in cart.__iter__(include_product=False):
            cart.add(item['id'], item['color_id'], user=request.user)
        return render(request, self.template_name, {'cart': cart})


def cart_products(request):
    cart = Cart(request)
    return render(request, 'partials/cart-partial.html', {'cart': cart})


def cart_prices(request):
    cart = Cart(request)
    return render(request, 'partials/price-partial.html', {'cart': cart})


class EmptyCart(View):
    template_name = 'partials/cart-partial.html'

    def get(self, request):
        cart = Cart(request)
        cart = cart.clear(request.user)
        html = render(request, self.template_name, {'cart': cart})
        response = {
            'html': html.content.decode('utf-8'),
            'cart_count': '0'
        }
        return JsonResponse(response)


class RemoveProduct(View):
    template_name = 'partials/cart-partial.html'

    def get(self, request):
        product_id = request.GET.get('product_id')
        color_id = request.GET.get('color_id')
        cart = Cart(request)
        cart.remove(product_id, color_id, request.user)
        html = render(request, self.template_name, {'cart': cart})
        response = {
            'html': html.content.decode('utf-8'),
            'cart_count': cart.count()
        }
        return JsonResponse(response)


class UpdateCount(View):
    template_name = 'partials/price-partial.html'

    def get(self, request):
        update_type = request.GET.get('type')
        product_id = request.GET.get('product_id')
        color_id = request.GET.get('color_id')
        cart = Cart(request)
        if update_type == 'increase':
            cart.increase(product_id, color_id, request.user)
        elif update_type == 'decrease':
            cart.decrease(product_id, color_id, request.user)
        html = render(request, self.template_name, {'cart': cart})
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


class Checkout(LoginRequiredMixin, View):
    template_name = 'cart_app/checkout.html'

    def get(self, request):
        cart = Cart(request)
        active_address = request.user.addresses.filter(is_active=True).first()
        context = {
            'cart': cart,
            'active_address': active_address
        }
        return render(request, self.template_name, context)


class SendRequest(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        amount = cart.get_payable_price() * 10
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": amount,
            "Description": settings.DESCRIPTION,
            "CallbackURL": settings.CALLBACKURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response_data = response.json()
                if response_data['Status'] == 100:
                    return redirect(settings.ZP_API_STARTPAY + response_data['Authority'])
                else:
                    return JsonResponse({'status': False, 'code': str(response_data['Status'])})
            return JsonResponse({'status': False, 'code': str(response.status_code)})
        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'code': 'connection error'})


class Verify(LoginRequiredMixin, View):
    template_name = 'cart_app/payment-confirm.html'

    def get(self, request):
        cart = Cart(request)
        amount = cart.get_payable_price() * 10
        authority = request.GET['Authority']
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": amount,
            "Authority": authority,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            status = request.GET['Status']
            authority = request.GET['Authority']
            if status == 'OK':
                cart = Cart(request)
                cart.clear()
                cart_model = CartModel.objects.filter(user=request.user, status='در انتظار پرداخت').first()
                cart_model.status = 'پرداخت شده'
                cart_model.payment_date = timezone.now()
                cart_model.authority = authority
                cart_model.save()
                context = {
                    'cart': cart_model,
                    'payment': True
                }
                return render(request, self.template_name, context)
            else:
                return redirect('CartApp:cart')
        return redirect('CartApp:cart')
