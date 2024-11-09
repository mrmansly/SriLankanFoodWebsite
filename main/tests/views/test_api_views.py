from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import MagicMock
from unittest.mock import patch
from django.urls import reverse
from main.models import Cart, CartItem, Product
import json
from main.fixtures.fixture_loader_utils import load_sample_session_cart
from ..security_testing_utils import get_authenticated_user
from rest_framework.test import APIClient


class ApiViewsTest(TestCase):

    def setUp(self):
        load_sample_session_cart()

    def create_sample_user_cart(self, user_id):
        cart = Cart.objects.create(user_id=user_id, session_id='oldSessionId')
        CartItem.objects.create(cart_id=cart.id, product_id=2, quantity=1, instructions='User Cart Item')

    @patch('main.views.api_views.add_product')
    def test_update_cart_item_api_with_matching_user(self, mock_add_product):

        user: User = get_authenticated_user()
        self.create_sample_user_cart(user.id)

        mock_add_product.return_value = None

        request_data = {
            'cart_id': '2',
            'product_id': 2,
            'quantity': 5,
            'instructions': 'No onions'
        }

        self.client = APIClient()
        self.client.force_authenticate(user=user)
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
