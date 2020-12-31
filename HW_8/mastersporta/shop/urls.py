from django.urls import path, include
from shop.views import shop_view, ShopView, shop_logout

urlpatterns = [
    path('', shop_view, name='shop'),
    path('api/', ShopView.as_view(), name='shop_api'),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', shop_logout, name='logout')
]
