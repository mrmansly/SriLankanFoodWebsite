from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Order
from main.serializers import OrderSerializer


class OrderViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.next_date = timezone.now() + timedelta(days=1)
        mobile = "+61418502888"

        # Set up data for the whole TestCase
        cls.active_order = Order.objects.create(
            # Fill in required fields
            first_name="First1",
            last_name="Last1",
            email="email1@discard.com",
            mobile=mobile,
            requested_delivery_date=cls.next_date,
            total_price=10,
            completed_date=None,
            cancelled_date=None
        )
        cls.completed_order = Order.objects.create(
            # Fill in required fields
            first_name="First2",
            last_name="Last2",
            email="email2@discard.com",
            mobile=mobile,
            total_price=20,
            requested_delivery_date=cls.next_date,
            completed_date=timezone.now(),
            cancelled_date=None
        )
        cls.cancelled_order = Order.objects.create(
            # Fill in required fields
            first_name="First3",
            last_name="Last3",
            email="email3@discard.com",
            mobile=mobile,
            requested_delivery_date=cls.next_date,
            total_price=30,
            completed_date=None,
            cancelled_date=timezone.now()
        )

    def test_list_orders(self):
        """Test retrieving a list of all orders."""
        url = reverse('order-list')
        response = self.client.get(url)
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_order(self):
        """Test creating a new order."""
        url = reverse('order-list')
        data = {
            'first_name': 'First4',
            'last_name': 'Last4',
            'email': 'email4@discard.com',
            'mobile': '0418590222',
            'requested_delivery_date': self.next_date,
            'total_price': '40',
            'completed_date': None,
            'cancelled_date': None,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 4)  # 3 from setUpTestData + 1 new

    def test_update_order(self):
        """Test updating an existing order."""
        url = reverse('order-detail', args=[self.active_order.id])
        data = {
            # Update fields as necessary
            'first_name': 'First4',
            'last_name': 'Last4',
            'email': 'email4@discard.com',
            'mobile': '0418590222',
            'requested_delivery_date': self.next_date,
            'total_price': '40',
            'completed_date': None,
            'cancelled_date': self.next_date,
        }
        response = self.client.put(url, data, format='json')
        self.active_order.refresh_from_db()  # Refresh instance with updated values
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.active_order.completed_date, None)
        self.assertEqual(self.active_order.cancelled_date, self.next_date)
        self.assertEqual(self.active_order.first_name, data['first_name'])
        self.assertEqual(self.active_order.last_name, data['last_name'])
        self.assertEqual(self.active_order.email, data['email'])
        self.assertEqual(self.active_order.mobile, '+61418590222')  # gets reformatted for consistency
        self.assertEqual(self.active_order.requested_delivery_date, self.next_date)
        self.assertEqual(self.active_order.total_price, 40)

    def test_partial_update_order(self):
        """Test partially updating an existing order."""
        url = reverse('order-detail', args=[self.completed_order.id])
        data = {
            'cancelled_date': self.next_date,
        }
        response = self.client.patch(url, data, format='json')
        self.completed_order.refresh_from_db()  # Refresh instance with updated values
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.completed_order.cancelled_date, self.next_date)

    def test_delete_order(self):
        """Test deleting an order."""
        url = reverse('order-detail', args=[self.cancelled_order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 2)  # 3 initial - 1 deleted

    def test_filter_orders_by_status_active(self):
        """Test filtering orders by 'active' status."""
        url = reverse('order-list')
        response = self.client.get(url, {'status': 'active'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.active_order.id)

    def test_filter_orders_by_status_completed(self):
        """Test filtering orders by 'completed' status."""
        url = reverse('order-list')
        response = self.client.get(url, {'status': 'completed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.completed_order.id)

    def test_filter_orders_by_status_cancelled(self):
        """Test filtering orders by 'cancelled' status."""
        url = reverse('order-list')
        response = self.client.get(url, {'status': 'cancelled'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.cancelled_order.id)
