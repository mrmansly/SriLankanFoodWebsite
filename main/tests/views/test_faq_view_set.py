from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from main.models import Faq, FaqCategory
from main.serializers import FaqSerializer
from ..security_testing_utils import get_authenticated_client


class FaqViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.faq_category = FaqCategory.objects.create(category="Category", description="Description")

        # Create initial data for tests
        cls.faq = Faq.objects.create(
            question="What is this FAQ?",
            answer="This is a test FAQ entry.",
            category=cls.faq_category
        )

    def test_list_faqs_when_unauthenticated(self):
        """Test retrieving the list of FAQs"""
        url = reverse('faq-list')  # Update with your viewset's URL name
        self.client = get_authenticated_client(False)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_faqs(self):
        """Test retrieving the list of FAQs"""
        url = reverse('faq-list')  # Update with your viewset's URL name
        self.client = get_authenticated_client()
        response = self.client.get(url)

        faqs = Faq.objects.all()
        serializer = FaqSerializer(faqs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_faq(self):
        """Test creating a new FAQ"""
        url = reverse('faq-list')  # Update with your viewset's URL name
        data = {"question": "How do I use this?", "answer": "This is how you use it.", "category": self.faq_category.id}
        self.client = get_authenticated_client()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Faq.objects.count(), 2)
        self.assertEqual(Faq.objects.get(id=response.data['id']).question, data["question"])
        self.assertEqual(Faq.objects.get(id=response.data['id']).answer, data["answer"])
        self.assertEqual(Faq.objects.get(id=response.data['id']).category_id, data["category"])

    def test_retrieve_faq(self):
        """Test retrieving a specific FAQ"""
        url = reverse('faq-detail', args=[self.faq.id])
        self.client = get_authenticated_client()
        response = self.client.get(url)

        serializer = FaqSerializer(self.faq)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_faq(self):
        """Test updating an existing FAQ"""
        url = reverse('faq-detail', args=[self.faq.id])

        new_faq_category = FaqCategory.objects.create(category="New Category", description="Desc")
        data = {"question": "Updated FAQ question", "answer": "Updated FAQ answer", "category": new_faq_category.id}
        self.client = get_authenticated_client()
        response = self.client.put(url, data, format='json')

        self.faq.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.faq.question, data["question"])
        self.assertEqual(self.faq.answer, data["answer"])
        self.assertEqual(self.faq.category_id, data["category"])

    def test_delete_faq(self):
        """Test deleting an FAQ"""
        url = reverse('faq-detail', args=[self.faq.id])
        self.client = get_authenticated_client()
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Faq.objects.count(), 0)
