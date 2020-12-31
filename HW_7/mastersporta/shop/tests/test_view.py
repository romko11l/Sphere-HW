from django.test import TestCase
from django.urls import reverse

from shop.models import Product
from shop.views import shop_view, ShopView

from collections import OrderedDict


class APITest(TestCase):
    def test_get(self):
        Product.objects.create(title='Ball', description='simple ball',
                               price=300)
        expect = {'products': [OrderedDict([('title', 'Ball'),
                                            ('description', 'simple ball'),
                                            ('price', 300)])]}
        resp = self.client.get(reverse('shop_api'))
        self.assertEqual(resp.data, expect)

    def test_post(self):
        pass

    def test_put(self):
        pass

    def test_delete(self):
        pass


class ViewsTest(TestCase):
    def test_shop(self):
        resp = self.client.get(reverse('shop'))
        self.assertEqual(resp.status_code, 200)
