from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from unittest.mock import patch
from django.urls import reverse
from main.models import Cart, CartItem
import json
from main.fixtures.fixture_loader_utils import load_sample_session_cart
from ..security_testing_utils import get_authenticated_user
from rest_framework.test import APIClient


class ApiViewsTest(TestCase):

    def setUp(self):
        # pass
        load_sample_session_cart()

    def create_sample_user_cart(self, user_id):
        cart = Cart.objects.create(user_id=user_id, session_id='oldSessionId')
        CartItem.objects.create(cart_id=cart.id, product_id=2, quantity=1, instructions='User Cart Item')

    def create_sample_session_cart(self, session_id):
        cart = Cart.objects.create(session_id=session_id)
        CartItem.objects.create(cart_id=cart.id, product_id=2, quantity=1, instructions='Session Cart Item')

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_add_product.assert_called_once_with(2,2,5,'No onions')

    def test_update_cart_item_api_with_matching_user_but_different_cart(self):

        user: User = get_authenticated_user()
        self.create_sample_user_cart(user.id)

        request_data = {
            'cart_id': '3',
            'product_id': 2,
            'quantity': 5,
            'instructions': 'No onions'
        }

        self.client = APIClient()
        self.client.force_authenticate(user=user)
        response = self.client.post(reverse('update_cart_item_api'), data=json.dumps(request_data), content_type='application/json', type=json)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    @patch('main.views.api_views.add_product')
    def test_update_cart_item_api_with_no_authenticated_user_but_with_matching_session(self, mock_add_product):

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_add_product.assert_called_once_with(2,2,5,'No onions')

    @patch('main.views.api_views.add_product')
    def test_update_cart_item_api_with_no_authenticated_user_but_matching_session_but_cart_mismatch(self, mock_add_product):

        user: User = get_authenticated_user()
        self.create_sample_user_cart(user.id)

        mock_add_product.return_value = None

        request_data = {
            'cart_id': '3',
            'product_id': 2,
            'quantity': 5,
            'instructions': 'No onions'
        }

        self.client = APIClient()
        self.client.force_authenticate(user=user)
        response = self.client.post(reverse('update_cart_item_api'), data=json.dumps(request_data), content_type='application/json', type=json)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('main.views.api_views.add_product')
    def test_update_cart_item_api_with_no_instructions(self, mock_add_product):

        user: User = get_authenticated_user()
        self.create_sample_user_cart(user.id)

        mock_add_product.return_value = None

        request_data = {
            'cart_id': '2',
            'product_id': 2,
            'quantity': 5
        }

        self.client = APIClient()
        self.client.force_authenticate(user=user)
        response = self.client.post(reverse('update_cart_item_api'), data=json.dumps(request_data), content_type='application/json', type=json)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_add_product.assert_called_once_with(2,2,5,None)
