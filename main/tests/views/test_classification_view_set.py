from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from main.models import Classification
from main.serializers import ClassificationSerializer
from ..security_testing_utils import get_authenticated_client


class ClassificationViewSetTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create initial data for tests
        cls.classification = Classification.objects.create(name="Test Classification", description="Description")

    def test_list_classification_when_unauthenticated(self):
        url = reverse('classification-list')  # Update with your viewset's URL name
        self.client = get_authenticated_client(False)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_classifications(self):
        """Test retrieving the list of classifications"""
        url = reverse('classification-list')  # Update with your viewset's URL name

        self.client = get_authenticated_client()
        response = self.client.get(url)

        classifications = Classification.objects.all()
        serializer = ClassificationSerializer(classifications, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_classification(self):
        """Test creating a new classification"""
        url = reverse('classification-list')  # Update with your viewset's URL name
        data = {"name": "New Classification", "description": "New Description"}
        self.client=get_authenticated_client()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Classification.objects.count(), 2)
        self.assertEqual(Classification.objects.get(id=response.data['id']).name, data["name"])
        self.assertEqual(Classification.objects.get(id=response.data['id']).description, data["description"])

    def test_retrieve_classification(self):
        """Test retrieving a specific classification"""
        url = reverse('classification-detail', args=[self.classification.id])
        self.client = get_authenticated_client()
        response = self.client.get(url)

        serializer = ClassificationSerializer(self.classification)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_classification(self):
        """Test updating an existing classification"""
        url = reverse('classification-detail', args=[self.classification.id])
        data = {"name": "Updated Classification", "description": "Updated Description"}
        self.client = get_authenticated_client()
        response = self.client.put(url, data, format='json')

        self.classification.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.classification.name, data["name"])
        self.assertEqual(self.classification.description, data["description"])

    def test_delete_classification(self):
        """Test deleting a classification"""
        url = reverse('classification-detail', args=[self.classification.id])
        self.client = get_authenticated_client()
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Classification.objects.count(), 0)
