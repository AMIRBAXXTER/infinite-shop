from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.http import JsonResponse
from django.shortcuts import render, redirect

from CartApp.cart import Cart
from CartApp.models import CartModel, CartItem
from ProductsApp.models import Product
from .forms import *
from .models import User


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = authenticate(phone=phone, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    cart_model = CartModel.objects.filter(user=user, status='1').first()
                    products = CartItem.objects.filter(cart=cart_model)
                    cart = Cart(request)
                    cart.clear()
                    cart = Cart(request)
                    for item in products:
                        cart.add(item.product.id, item.color_id, item.quantity)
                    return redirect('UserApp:profile')

    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(phone=cd['phone'], password=cd['password'], first_name=cd['first_name'],
                                     last_name=cd['last_name'])
            user = authenticate(phone=cd['phone'], password=cd['password'])
            login(request, user)
            cart = Cart(request)
            for item in cart.__iter__(include_product=False):
                cart.new_user_add(item['id'], item['color_id'], item['quantity'], user=request.user)
            return redirect('IndexApp:index')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def user_profile(request):
    user = request.user
    context = {
        'user': user
    }
    if request.method == 'POST':
        form_name = request.POST.get('form_name')
        if form_name == 'profile_form':
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('UserApp:profile')
            else:
                context.update({
                    'profile_form': profile_form,
                    'password_form': PasswordChangeForm(),
                })
        if form_name == 'password_form':
            password_form = PasswordChangeForm(request.POST, request=request)
            if password_form.is_valid():
                cd = password_form.cleaned_data
                old_password = cd['old_password']
                new_password = cd['new_password2']
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    login(request, user)
                    context.update({
                        'profile_form': UserProfileForm(instance=user),
                        'password_form': password_form,
                    })
                    return redirect('UserApp:profile')
                else:
                    context.update({
                        'profile_form': UserProfileForm(instance=user),
                        'password_form': password_form,
                    })
            else:
                context.update({
                    'profile_form': UserProfileForm(instance=user),
                    'password_form': password_form,
                })
    else:
        context.update({
            'profile_form': UserProfileForm(instance=user),
            'password_form': PasswordChangeForm(),
        })
    return render(request, 'profile/profile.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect('UserApp:login')


@login_required
def favorite_products(request):
    fav_products = Product.objects.filter(favorites__user=request.user).order_by('-created_at')
    context = {
        'fav_products': fav_products
    }
    return render(request, 'profile/favorites.html', context)

@login_required
def factors(request):
    user_carts = CartModel.objects.filter(user=request.user).all().order_by('-created_at')
    context = {
        'user_carts': user_carts
    }
    return render(request, 'profile/factors.html', context)


def addresses(request):
    form = AddressForm()
    context = {
        'form': form
    }
    return render(request, 'profile/addresses.html', context)


def address_partial(request):
    user_addresses = request.user.addresses.all()
    context = {
        'user_addresses': user_addresses
    }
    return render(request, 'partials/user-address-partial.html', context)


def form_partial(request):
    form = AddressForm()
    context = {
        'form': form
    }
    return render(request, 'partials/address-form.html', context)


def get_city(request):
    province_id = request.GET.get('province_id')
    province = Province.objects.get(id=province_id)
    cities = list(City.objects.filter(province=province).all().order_by('name').values_list('name', 'id'))
    response = {
        'cities': cities
    }
    return JsonResponse(response)


def add_address(request):
    submit_type = request.GET.get('submit_type')
    if submit_type == 'add':
        form = AddressForm(request.GET)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
        else:
            context = {
                'form': form
            }
            return render(request, 'partials/address-form.html', context)
    elif submit_type == 'edit':
        address_id = request.GET.get('address_id')
        address = Address.objects.get(id=address_id)
        form = AddressForm(request.GET, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
        else:
            context = {
                'form': form
            }
            return render(request, 'partials/address-form.html', context)
    user_addresses = request.user.addresses.all().order_by('-created_at')
    context = {
        'user_addresses': user_addresses
    }
    return render(request, 'partials/user-address-partial.html', context)


def delete_address(request):
    address_id = request.GET.get('address_id')
    address = Address.objects.get(id=address_id)
    address.delete()
    user_addresses = request.user.addresses.all().order_by('-created_at')
    context = {
        'user_addresses': user_addresses
    }
    return render(request, 'partials/user-address-partial.html', context)


def activate_address(request):
    address_id = request.GET.get('address_id')
    address = Address.objects.get(id=address_id)
    address.is_active = True
    address.save()
    user_addresses = request.user.addresses.all().order_by('-created_at')
    context = {
        'user_addresses': user_addresses
    }
    return render(request, 'partials/user-address-partial.html', context)


def edit_address(request):
    address_id = request.GET.get('address_id')
    address = Address.objects.get(id=address_id)
    form = AddressForm(instance=address)
    context = {
        'form': form,
    }
    return render(request, 'partials/address-form.html', context)
