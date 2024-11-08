from django.test import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
from django.urls import reverse
# from main.models import Cart, CartItem, Product
import json
from main.fixtures.fixture_loader_utils import load_sample_cart


class TestApiViews(TestCase):

    def setUp(self):
        load_sample_cart()

    @patch('main.views.api_views.add_product')
    def test_api_gateway_update_cart_item_quantity(self,
                                                   mock_add_product):

        mock_add_product.return_value = None

        request_data = {
            'cart_id': '1',
            'product_id': 2,
            'quantity': 5,
            'instructions': 'No onions'
        }

        response = self.client.post(reverse('update_cart_item_api'), data=json.dumps(request_data), content_type='application/json', type=json)

        # Assert
        self.assertEqual(response.status_code, 200)

    @patch('main.views.api_views.add_product')
    def test_api_gateway_update_cart_item_quantity_with_no_instructions(self,
                                                   mock_add_product):

        mock_add_product.return_value = None

        request_data = {
            'cart_id': '1',
            'product_id': 2,
            'quantity': 5
        }

        response = self.client.post(reverse('update_cart_item_api'), data=json.dumps(request_data), content_type='application/json', type=json)

        # Assert
        self.assertEqual(response.status_code, 200)
        mock_add_product.assert_called_once_with(1,2,5,None)
