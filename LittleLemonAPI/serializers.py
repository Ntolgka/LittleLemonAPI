from decimal import Decimal
from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'stock',
                  'price_after_tax', 'category', 'category_id']

        extra_kwargs = {
            'price': {'min_value': 1},
        }

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'user_permissions']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'quantity', 'unit_price', 'price', 'menuitem']
        read_only_fields = ['user', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total', 'user']


#   Commented to use Model Serializers instead
# class MenuItemSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     inventory = serializers.IntegerField()
