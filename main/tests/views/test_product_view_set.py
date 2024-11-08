from rest_framework.test import APITestCase
from rest_framework import status
from main.models import Product
from main.serializers import ProductSerializer


class ProductViewSetTestCase(APITestCase):
    def setUp(self):
        """
        Set up test data, including any initial Product objects that can be used in tests.
        """
        self.product_data = {
            'name': 'Test Product',
            'description': 'A description of the test product',
            'price': 100.0,
        }

        self.product = Product.objects.create(**self.product_data)
        self.url = '/api/products/'  # Update this with your actual API endpoint path

    def test_product_list(self):
        """
        Test the list view of the ProductViewSet (GET /api/products/).
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure the product list includes the product we created
        self.assertEqual(len(response.data), 1)  # Only 1 product should be in the list
        self.assertEqual(response.data[0]['name'], self.product.name)

    def test_product_create(self):
        """
        Test the create view of the ProductViewSet (POST /api/products/).
        """
        new_product_data = {
            'name': 'New Product',
            'description': 'Description for the new product',
            'price': 150.0
        }
        response = self.client.post(self.url, new_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify that the product is created and the response data is correct
        self.assertEqual(response.data['name'], new_product_data['name'])
        self.assertEqual(response.data['description'], new_product_data['description'])
        self.assertEqual(response.data['price'], new_product_data['price'])

    def test_product_detail(self):
        """
        Test the detail view of the ProductViewSet (GET /api/products/{id}/).
        """
        response = self.client.get(f'{self.url}{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that the correct product is returned
        self.assertEqual(response.data['name'], self.product.name)
        self.assertEqual(response.data['description'], self.product.description)
        self.assertEqual(response.data['price'], self.product.price)

    def test_product_update(self):
        """
        Test the update view of the ProductViewSet (PUT /api/products/{id}/).
        """
        updated_product_data = {
            'name': 'Updated Product',
            'description': 'Updated description',
            'price': 120.0
        }
        response = self.client.put(f'{self.url}{self.product.id}/', updated_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that the product data has been updated
        self.assertEqual(response.data['name'], updated_product_data['name'])
        self.assertEqual(response.data['description'], updated_product_data['description'])
        self.assertEqual(response.data['price'], updated_product_data['price'])

    def test_product_delete(self):
        """
        Test the delete view of the ProductViewSet (DELETE /api/products/{id}/).
        """
        response = self.client.delete(f'{self.url}{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify that the product has been deleted
        self.assertEqual(Product.objects.count(), 0)

    def test_invalid_product_create(self):
        """
        Test creating a product with invalid data (e.g., missing required fields).
        """
        invalid_product_data = {
            'name': '',  # Empty name should not be valid
            'description': 'A product with no name',
            'price': 100.0
        }
        response = self.client.post(self.url, invalid_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verify that the response contains an error related to the 'name' field
        self.assertIn('name', response.data)
