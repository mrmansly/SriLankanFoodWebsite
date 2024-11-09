from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from ..security_testing_utils import get_access_token, get_authenticated_user
from django.urls import reverse
from main.models import Cart
from unittest import mock
from main.serializers import CartSerializer


class CartViewSetTest(APITestCase):

    def setUp(self):

        # Set up the APIClient and log in the to allow API to be called
        self.client = APIClient()
        self.client.force_authenticate(user=get_authenticated_user())

        self.cart = Cart.objects.create(session_id="sessionId")

        # Set the endpoint URL for convenience
        self.list_url = reverse('cart-list')  # This assumes you have a named route for CartViewSet

    # Add a test for checking API unauthorised access
    def test_list_carts_when_unauthenticated(self):

        with mock.patch.object(self, 'setUp', lambda x: None):
            self.client = APIClient()
            self.client.force_authenticate(user=None)
            self.list_url = reverse('cart-list')

            """Test the list endpoint of the CartViewSet is blocked"""
            response = self.client.get(self.list_url)

            # Assert that the response is 401 Unauthorised
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_carts(self):
        """Test the list endpoint of the CartViewSet"""
        response = self.client.get(self.list_url)
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)

        # Assert that the response is 200 OK and data matches
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_cart(self):
        """Test the retrieve endpoint of the CartViewSet"""
        retrieve_url = reverse('cart-detail', args=[self.cart.id])
        response = self.client.get(retrieve_url)

        serializer = CartSerializer(self.cart)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_cart(self):
        """Test the create endpoint of the CartViewSet"""
        data = {
            "session_id": "test_session_12345",
            "user": None
        }
        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Cart.objects.filter(session_id="test_session_12345").exists())

    def test_update_cart(self):
        """Test the update endpoint of the CartViewSet"""
        update_url = reverse('cart-detail', args=[self.cart.id])
        data = {
            "session_id": "updated_session_id"
        }
        response = self.client.put(update_url, data, format='json')

        # Refresh the cart instance from the database to check updated fields
        self.cart.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.cart.session_id, "updated_session_id")

    def test_delete_cart(self):
        """Test the delete endpoint of the CartViewSet"""
        delete_url = reverse('cart-detail', args=[self.cart.id])
        response = self.client.delete(delete_url)

        # Ensure that the cart was deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cart.objects.filter(id=self.cart.id).exists())
