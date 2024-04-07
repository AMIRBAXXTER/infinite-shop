from django.test import TestCase
from django.urls import reverse, resolve
from CartApp.views import *


class TestUrls(TestCase):
    def test_urls(self):
        urls = [
            reverse('CartApp:cart'),
            reverse('CartApp:add_to_cart'),
            reverse('CartApp:remove_product'),
            reverse('CartApp:empty_cart'),
            reverse('CartApp:update_count'),
            reverse('CartApp:checkout'),
            reverse('CartApp:send_request'),
            reverse('CartApp:verify'),
        ]
        views = [
            cart,
            add_to_cart,
            remove_product,
            empty_cart,
            update_count,
            checkout,
            send_request,
            verify,
        ]
        for url, view in zip(urls, views):
            self.assertEqual(resolve(url).func, view)
