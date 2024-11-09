from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from main.models import Contact, ContactType, ContactTypeEnum
from main.serializers import ContactSerializer
from ..security_testing_utils import get_authenticated_client


class ContactViewSetTests(APITestCase):

    def setUp(self):

        self.reviewContactType = ContactType.objects.create(type=ContactTypeEnum.REVIEW.value,
                                                      description='Review Contact Type')

        # id of this contact type must match with ContactTypeEnum value of 2, hence why contact type above
        # was also created
        self.feedbackContactType = ContactType.objects.create(type=ContactTypeEnum.FEEDBACK.value,
                                                            description='Review Contact Type')

        # Set up initial data for tests
        self.contact1 = Contact.objects.create(type=self.feedbackContactType, title="Contact1", message="message1")
        self.contact2 = Contact.objects.create(type=self.feedbackContactType, title="Contact2", message="message2")
        self.list_url = reverse('contact-list')

    def test_list_contacts_when_unauthenticated(self):
        self.client = get_authenticated_client(False)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_contacts(self):
        # Test retrieving all contacts
        self.client = get_authenticated_client()
        response = self.client.get(self.list_url)
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_contact(self):
        # Test retrieving a single contact by ID
        url = reverse('contact-detail', args=[self.contact1.id])
        self.client = get_authenticated_client()
        response = self.client.get(url)
        serializer = ContactSerializer(self.contact1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_contact(self):
        # Test creating a new contact
        data = {
            'type': self.feedbackContactType.id,
            'title': 'New Contact',
            'message': 'Message'
        }
        self.client = get_authenticated_client()
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 3)
        self.assertEqual(Contact.objects.last().title, 'New Contact')

    def test_update_contact(self):
        # Test updating an existing contact
        url = reverse('contact-detail', args=[self.contact1.id])
        data = {
            'type': self.reviewContactType.id,
            'title': 'New Title',
            'message': 'New Message',
            'rating': '2'
        }
        self.client = get_authenticated_client()
        response = self.client.put(url, data, format='json')
        self.contact1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.contact1.message, 'New Message')
        self.assertEqual(self.contact1.type, self.reviewContactType)
        self.assertEqual(self.contact1.rating, 2)
        self.assertEqual(self.contact1.title, 'New Title')

    def test_partial_update_contact(self):
        # Test partially updating an existing contact (PATCH)
        url = reverse('contact-detail', args=[self.contact2.id])
        data = {'message': 'Janet Smith'}
        self.client = get_authenticated_client()
        response = self.client.patch(url, data, format='json')
        self.contact2.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.contact2.message, 'Janet Smith')

    def test_delete_contact(self):
        # Test deleting a contact
        url = reverse('contact-detail', args=[self.contact1.id])
        self.client = get_authenticated_client()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertFalse(Contact.objects.filter(id=self.contact1.id).exists())
