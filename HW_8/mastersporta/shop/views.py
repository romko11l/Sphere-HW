from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

from .models import Product
from .serializers import ProductSerializer

from captcha.fields import ReCaptchaField

import json


@login_required
def shop_view(request):
    """Main page render"""
    posts = Product.objects.all()[::-1]
    return render(request, 'index.html',
                  context={'posts': posts, 'username': request.user.username})


@login_required
def shop_logout(request):
    """Logout button implementation"""
    logout(request)
    return HttpResponseRedirect(reverse('auth'))


def auth_check(func):
    """Check authentication for REST API"""
    def wrapper(self, request):
        if request.user.is_authenticated:
            return func(self, request)
        else:
            return HttpResponseRedirect(reverse('auth'))
    return wrapper


class ShopView(APIView):
    """Implementation CRUD api operation"""
    @auth_check
    def get(self, request):
        """Returns the entire list of products as json"""
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data})

    @auth_check
    def post(self, request):
        """Updates product with the passed id"""
        with open('/home/roman/work/log.txt', 'a') as log:
            log.write(json.dumps(request.COOKIES))
        product_id = request.data.get('id')
        saved_product = get_object_or_404(Product.objects.all(), pk=product_id)
        data = request.data.get('product')
        serializer = ProductSerializer(instance=saved_product, data=data,
                                       partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(status=200)
        return Response(status=404)

    @auth_check
    def put(self, request):
        """Adds a new product to the store"""
        with open('/home/roman/work/log.txt', 'a') as log:
            log.write(json.dumps(request.COOKIES))
        new_product = request.data.get('product')
        serializer = ProductSerializer(data=new_product)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(status=200)
        return Response(status=404)

    @auth_check
    def delete(self, request):
        """Delete the product with the passed id"""
        product_id = request.data.get('id')
        saved_product = get_object_or_404(Product.objects.all(), pk=product_id)
        saved_product.delete()
        return Response(status=200)
