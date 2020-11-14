from django.urls import path, include
from shop.views import shop_view, ShopView

urlpatterns = [
    path('', shop_view, name='shop'),
    path('api/', ShopView.as_view(), name='shop_api')
]
