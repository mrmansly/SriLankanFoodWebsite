from rest_framework import serializers
from .models import Cart, CartItem, Contact, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(many=False,read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):

    cart_items = CartItemSerializer(many=True,read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
