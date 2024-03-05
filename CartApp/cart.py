from django.http import HttpRequest, Http404

from ProductsApp.models import Product, ProductColor


class Cart:
    def __init__(self, request: HttpRequest):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id: int, product_color_id: int, count: int = 1):
        product: Product = Product.objects.get(id=product_id)
        product_color = ProductColor.objects.get(id=product_color_id, product=product)
        if f'{product_id},{product_color_id}' not in self.cart:
            if int(product_color.stock) >= int(count):
                self.cart[f'{product_id},{product_color_id}'] = {
                    'id': product.id,
                    'color_id': product_color.id,
                    'price': product.price,
                    'final_price': product.final_price,
                    'color': product_color.color,
                    'weight': product.weight,
                    'quantity': count,
                }

        self.save()

    def decrease(self, product_id: int, product_color_id: int):
        if self.cart[f'{product_id},{product_color_id}']['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1
        self.save()

    def remove(self, product_id: int, product_color_id: int):
        if self.cart[f'{product_id},{product_color_id}']:
            del self.cart[f'{product_id},{product_color_id}']
        self.save()

    def clear(self):
        del self.session['cart']
        self.save()

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

    def get_off_price(self):
        return sum(
            (int(item['price']) - int(item['final_price'])) * int(item['quantity']) for item in self.cart.values())

    def get_final_price(self):
        return self.get_products_price() + self.get_post_price()

    def get_payable_price(self):
        return self.get_final_price() - self.get_off_price()

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def __iter__(self):
        for item in self.cart.values():
            product_id = item['id']
            product = Product.objects.get(id=product_id)
            item['product'] = product
            yield item

    def __str__(self):
        return str(self.cart)

    def save(self):
        self.session.modified = True
