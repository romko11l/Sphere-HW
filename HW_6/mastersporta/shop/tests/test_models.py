from django.test import TestCase

from shop.models import Product


class ModelsTest(TestCase):
    def test_product(self):
        Product.objects.create(title='Ball', description='simple ball',
                               price=300)
        ball = Product.objects.get(id=1)
        self.assertEquals(ball.title, 'Ball')
        self.assertEquals(ball.description, 'simple ball')
        self.assertEquals(ball.price, 300)
        field_label = ball._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'Название товара')
        field_label = ball._meta.get_field('description').verbose_name
        self.assertEquals(field_label,'Описание товара')
        field_label = ball._meta.get_field('price').verbose_name
        self.assertEquals(field_label,'Цена товара')
        max_length = ball._meta.get_field('title').max_length
        self.assertEquals(max_length, 128)
