from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.Serializer):
    """Serializer for Product"""
    title = serializers.CharField(max_length=128)
    description = serializers.CharField()
    price = serializers.IntegerField()

    def create(self, data):
        """Helper function for put api methods"""
        return Product.objects.create(**data)

    def update(self, instance, data):
        """Helper function for post api methods"""
        instance.title = data.get('title', instance.title)
        instance.description = data.get('description', instance.description)
        instance.price = data.get('price', instance.price)
        instance.save()
        return instance
