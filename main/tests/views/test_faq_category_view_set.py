from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from main.models import FaqCategory
from main.serializers import FaqCategorySerializer
from ..security_testing_utils import get_authenticated_client


class FaqCategoryViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create initial data for tests
        cls.faq_category = FaqCategory.objects.create(category="General FAQs", description="FAQ Description")

    def test_list_faq_categories_when_unauthenticated(self):
        """Test retrieving the list of FAQ categories"""
        url = reverse('faq-category-list')  # Update with your viewset's URL name
        self.client = get_authenticated_client(False)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_faq_categories(self):
        """Test retrieving the list of FAQ categories"""
        url = reverse('faq-category-list')  # Update with your viewset's URL name
        self.client = get_authenticated_client()
        response = self.client.get(url)

        faq_categories = FaqCategory.objects.all()
        serializer = FaqCategorySerializer(faq_categories, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_faq_category(self):
        """Test creating a new FAQ category"""
        url = reverse('faq-category-list')  # Update with your viewset's URL name
        data = {"category": "New FAQ Category", "description": "New Description"}
        self.client = get_authenticated_client()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FaqCategory.objects.count(), 2)
        self.assertEqual(FaqCategory.objects.get(id=response.data['id']).category, data["category"])
        self.assertEqual(FaqCategory.objects.get(id=response.data['id']).description, data["description"])

    def test_retrieve_faq_category(self):
        """Test retrieving a specific FAQ category"""
        url = reverse('faq-category-detail', args=[self.faq_category.id])
        self.client = get_authenticated_client()
        response = self.client.get(url)

        serializer = FaqCategorySerializer(self.faq_category)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_faq_category(self):
        """Test updating an existing FAQ category"""
        url = reverse('faq-category-detail', args=[self.faq_category.id])
        data = {"category": "Updated FAQ Category", "description": "Updated Description"}
        self.client = get_authenticated_client()
        response = self.client.put(url, data, format='json')

        self.faq_category.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.faq_category.category, data["category"])
        self.assertEqual(self.faq_category.description, data["description"])

    def test_delete_faq_category(self):
        """Test deleting an FAQ category"""
        url = reverse('faq-category-detail', args=[self.faq_category.id])
        self.client = get_authenticated_client()
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FaqCategory.objects.count(), 0)
