from django.db import models


class Product(models.Model):
    title = models.CharField('Название товара', max_length=128, null=False)
    description = models.TextField('Описание товара', null=True)
    price = models.IntegerField("Цена товара", null=False)
