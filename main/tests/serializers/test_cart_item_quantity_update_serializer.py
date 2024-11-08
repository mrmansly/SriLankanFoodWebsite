from rest_framework import serializers
from django.test import TestCase
from main.serializers import CartItemQuantityUpdateSerializer


class CartItemQuantityUpdateSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'cart_id': 1,
            'product_id': 100,
            'quantity': 5,
            'instructions': "Please pack with care."
        }

    def test_serializer_with_valid_data(self):
        serializer = CartItemQuantityUpdateSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['cart_id'], self.valid_data['cart_id'])
        self.assertEqual(serializer.validated_data['product_id'], self.valid_data['product_id'])
        self.assertEqual(serializer.validated_data['quantity'], self.valid_data['quantity'])
        self.assertEqual(serializer.validated_data['instructions'], self.valid_data['instructions'])

    def test_serializer_with_missing_instructions(self):
        data = self.valid_data.copy()
        data.pop('instructions')
        serializer = CartItemQuantityUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('instructions', serializer.validated_data)  # Optional field

    def test_serializer_with_blank_instructions(self):
        data = self.valid_data.copy()
        data['instructions'] = ""
        serializer = CartItemQuantityUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['instructions'], "")

    def test_serializer_with_null_instructions(self):
        data = self.valid_data.copy()
        data['instructions'] = None
        serializer = CartItemQuantityUpdateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertIsNone(serializer.validated_data['instructions'])

    def test_serializer_with_negative_quantity(self):
        data = self.valid_data.copy()
        data['quantity'] = -1  # Invalid quantity
        serializer = CartItemQuantityUpdateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_serializer_with_missing_required_field(self):
        data = self.valid_data.copy()
        data.pop('product_id')  # Missing required field
        serializer = CartItemQuantityUpdateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('product_id', serializer.errors)
