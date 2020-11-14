from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from .models import Product
from .serializers import ProductSerializer


def shop_view(request):
    """Main page render"""
    posts = Product.objects.all()[::-1]
    return render(request, 'index.html', context={'posts': posts})


class ShopView(APIView):
    """Implementation CRUD api operation"""
    def get(self, request):
        """Returns the entire list of products as json"""
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data})

    def post(self, request):
        """Updates product with the passed id"""
        product_id = request.data.get('id')
        saved_product = get_object_or_404(Product.objects.all(), pk=product_id)
        data = request.data.get('product')
        serializer = ProductSerializer(instance=saved_product, data=data,
                                       partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(status=200)
        return Response(status=404)

    def put(self, request):
        """Adds a new product to the store"""
        new_product = request.data.get('product')
        serializer = ProductSerializer(data=new_product)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(status=200)
        return Response(status=404)

    def delete(self, request):
        """Delete the product with the passed id"""
        product_id = request.data.get('id')
        saved_product = get_object_or_404(Product.objects.all(), pk=product_id)
        saved_product.delete()
        return Response(status=200)
