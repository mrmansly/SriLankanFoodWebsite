from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from main.models import ContactType, ContactTypeEnum
from main.serializers import ContactTypeSerializer


class ContactTypeViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create initial data for tests
        cls.contact_type = ContactType.objects.create(type='Review Type',
                                                      description="Review Description")

    def test_list_contact_types(self):
        """Test retrieving the list of contact types"""
        url = reverse('contact-type-list')  # Update with your viewset's URL name
        response = self.client.get(url)

        contact_types = ContactType.objects.all()
        serializer = ContactTypeSerializer(contact_types, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_contact_type(self):
        """Test creating a new contact type"""
        url = reverse('contact-type-list')  # Update with your viewset's URL name
        data = {"type": 'Feedback Type', "description": "Feedback"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactType.objects.count(), 2)
        self.assertEqual(ContactType.objects.get(id=response.data['id']).type, data["type"])
        self.assertEqual(ContactType.objects.get(id=response.data['id']).description, data["description"])

    def test_retrieve_contact_type(self):
        """Test retrieving a specific contact type"""
        url = reverse('contact-type-detail', args=[self.contact_type.id])
        response = self.client.get(url)

        serializer = ContactTypeSerializer(self.contact_type)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_contact_type(self):
        """Test updating an existing contact type"""
        url = reverse('contact-type-detail', args=[self.contact_type.id])
        data = {"type": 'Website Type', "description": "Website"}
        response = self.client.put(url, data, format='json')

        self.contact_type.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.contact_type.type, data["type"])
        self.assertEqual(self.contact_type.description, data["description"])

    def test_delete_contact_type(self):
        """Test deleting a contact type"""
        url = reverse('contact-type-detail', args=[self.contact_type.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContactType.objects.count(), 0)