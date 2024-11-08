from rest_framework import serializers
from .models import Cart, CartItem, Contact, Product, Classification, ContactType, FaqCategory, Faq, Order


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


class ContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactType
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):

    type = ContactTypeSerializer

    class Meta:
        model = Contact
        fields = '__all__'


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = '__all__'


class FaqCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqCategory
        fields = '__all__'


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CartItemQuantityUpdateSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=0)
    instructions = serializers.CharField(required=False, allow_blank=True, allow_null=True)
