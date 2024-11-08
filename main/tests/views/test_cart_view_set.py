from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from main.models import Cart, User
from main.serializers import CartSerializer


class CartViewSetTests(APITestCase):

    def setUp(self):
        # Create a user and a cart associated with that user
        self.user = User.objects.create(user_name='testuser', password='testpassword')
        self.cart = Cart.objects.create(user=self.user)

        # Set up the APIClient and log in the user if needed
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Set the endpoint URL for convenience
        self.list_url = reverse('cart-list')  # This assumes you have a named route for CartViewSet

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
            "user": self.user.id,
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
