from django.http import HttpRequest, Http404

from CartApp.models import CartModel, CartItem
from ProductsApp.models import Product, ProductColor
from UserApp.models import User


class Cart:
    def __init__(self, request: HttpRequest):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id: int, product_color_id: int, count: int = 1, user: User = None):
        product: Product = Product.objects.get(id=product_id)
        product_color = ProductColor.objects.get(id=product_color_id, product=product)
        cart_key = f'{product_id},{product_color_id}'

        if cart_key not in self.cart:
            if int(product_color.stock) >= int(count):
                self.cart[cart_key] = {
                    'id': product.id,
                    'color_id': product_color.id,
                    'price': product.price,
                    'final_price': product.final_price,
                    'color': product_color.color,
                    'color_stock': product_color.stock,
                    'weight': product.weight,
                    'quantity': int(count),
                }
                self.save()
            if user is not None:
                if user.is_authenticated:
                    address_id = user.addresses.filter(is_active=True).first().id
                    cart_model, created = CartModel.objects.get_or_create(user=user, address_id=address_id)
                    cart_item = CartItem.objects.create(cart=cart_model, product=product, color_id=product_color.id,
                                                        price=product.price, final_price=product.final_price,
                                                        color=product_color.color, color_stock=product_color.stock,
                                                        weight=product.weight, quantity=int(count))
                    cart_item.save()
                    cart_model.final_price = self.get_payable_price()
                    cart_model.save()
        else:
            self.cart[cart_key]['price'] = product.price
            self.cart[cart_key]['final_price'] = product.final_price
            self.cart[cart_key]['weight'] = product.weight
            self.cart[cart_key]['color_stock'] = product_color.stock

            self.save()
            if user is not None:
                if user.is_authenticated:
                    cart_model = CartModel.objects.filter(user=user, status='در انتظار پرداخت').first()
                    cart_item = CartItem.objects.get(cart=cart_model, product=product, color_id=product_color.id)
                    cart_item.price = product.price
                    cart_item.final_price = product.final_price
                    cart_item.weight = product.weight
                    cart_item.color_stock = product_color.stock
                    cart_item.save()
                    cart_model.final_price = self.get_payable_price()
                    cart_model.save()

    def new_user_add(self, product_id: int, product_color_id: int, count: int = 1, user: User = None):
        product: Product = Product.objects.get(id=product_id)
        product_color = ProductColor.objects.get(id=product_color_id, product=product)

        cart_model, created = CartModel.objects.get_or_create(user=user, status='در انتظار پرداخت')
        if int(product_color.stock) >= int(count):
            cart_item = CartItem.objects.create(cart=cart_model, product=product, color_id=product_color.id,
                                                price=product.price, final_price=product.final_price,
                                                color=product_color.color, color_stock=product_color.stock,
                                                weight=product.weight, quantity=int(count))
            cart_item.save()
            cart_model.final_price = self.get_payable_price()
            cart_model.save()

    def increase(self, product_id: int, product_color_id: int, user: User = None):
        product = Product.objects.get(id=product_id)
        product_color = ProductColor.objects.get(id=product_color_id, product=product)
        if int(self.cart[f'{product_id},{product_color_id}']['quantity']) < int(product_color.stock):
            self.cart[f'{product_id},{product_color_id}']['quantity'] += 1
            self.save()
            if user is not None:
                if user.is_authenticated:
                    product = Product.objects.get(id=product_id)
                    product_color = ProductColor.objects.get(id=product_color_id, product=product)
                    cart_model = CartModel.objects.filter(user=user, status='در انتظار پرداخت').first()
                    cart_item = CartItem.objects.get(cart=cart_model, product=product, color_id=product_color.id)
                    cart_item.quantity += 1
                    cart_item.save()
                    cart_model.final_price = self.get_payable_price()
                    cart_model.save()

    def decrease(self, product_id: int, product_color_id: int, user: User = None):

        if int(self.cart[f'{product_id},{product_color_id}']['quantity']) > 1:
            self.cart[f'{product_id},{product_color_id}']['quantity'] -= 1
            self.save()
            if user is not None:
                if user.is_authenticated:
                    product = Product.objects.get(id=product_id)
                    product_color = ProductColor.objects.get(id=product_color_id, product=product)
                    cart_model = CartModel.objects.filter(user=user, status='در انتظار پرداخت').first()
                    cart_item = CartItem.objects.get(cart=cart_model, product=product, color_id=product_color.id)
                    cart_item.quantity -= 1
                    cart_item.save()
                    cart_model.final_price = self.get_payable_price()
                    cart_model.save()

    def remove(self, product_id: int, product_color_id: int, user: User = None):
        if self.cart[f'{product_id},{product_color_id}']:
            del self.cart[f'{product_id},{product_color_id}']
        self.save()
        if user is not None:
            if user.is_authenticated:
                product = Product.objects.get(id=product_id)
                product_color = ProductColor.objects.get(id=product_color_id, product=product)
                cart_model = CartModel.objects.filter(user=user, status='در انتظار پرداخت').first()
                cart_item = CartItem.objects.get(cart=cart_model, product=product, color_id=product_color.id)
                cart_item.delete()
                cart_model.final_price = self.get_payable_price()
                cart_model.save()

    def clear(self, user: User = None):
        del self.session['cart']
        self.save()
        if user is not None:
            if user.is_authenticated:
                cart_model = CartModel.objects.filter(user=user, status='در انتظار پرداخت').first()
                cart_model.delete()

    def get_post_price(self):
        weight = sum(int(item['weight']) * int(item['quantity']) for item in self.cart.values())
        if weight == 0:
            return 0
        elif 0 < weight < 1000:
            return 35000
        elif 1000 <= weight <= 2000:
            return 50000
        else:
            return 75000

    def get_products_price(self):
        return sum(int(item['price']) * int(item['quantity']) for item in self.cart.values())

    def get_off_price(self, product_id, product_color_id):
        return (int(self.cart[f'{product_id},{product_color_id}']['price']) - int(
            self.cart[f'{product_id},{product_color_id}']['final_price'])) * int(
            self.cart[f'{product_id},{product_color_id}']['quantity'])

    def get_total_off_price(self):
        return sum(
            (int(item['price']) - int(item['final_price'])) * int(item['quantity']) for item in self.cart.values())

    def get_final_price(self, product_id, product_color_id):
        return int(self.cart[f'{product_id},{product_color_id}']['final_price']) * int(
            self.cart[f'{product_id},{product_color_id}']['quantity'])

    def get_total_final_price(self):
        return self.get_products_price() + self.get_post_price()

    def get_payable_price(self):
        return self.get_total_final_price() - self.get_total_off_price()

    def count(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def __iter__(self, include_product=True):
        for item in self.cart.values():
            if include_product:
                product_id = item['id']
                product = Product.objects.get(id=product_id)
                item['product'] = product
            yield item

    def __str__(self):
        return str(self.cart)

    def save(self):
        self.session.save()

    def copy(self):
        return self.cart.copy()
