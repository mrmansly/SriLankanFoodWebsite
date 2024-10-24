from django.test import TestCase
from main.forms import CheckoutForm, ContactForm
from django.utils import timezone
from main.models import ContactType
from datetime import timedelta


class TestForms(TestCase):

    def setUp(self):
        self.contact_type = ContactType.objects.create(
            id=1,
            type='REVIEW',
            description='description'
        )

    def test_checkout_form_valid(self):
        form = CheckoutForm(data={
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'email@discard.com',
            'mobile': '0433333333',
            'home_phone': '+61894571664',
            'requested_delivery_date': timezone.now() + timedelta(days=2)
        })
        self.assertTrue(form.is_valid())

    def test_checkout_form_mobile_invalid(self):
        form = CheckoutForm(data={
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'email@discard.com',
            'mobile': '000000000',
            'home_phone': '+61894571664',
            'requested_delivery_date': timezone.now()
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_checkout_form_home_phone_invalid(self):
        form = CheckoutForm(data={
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'email@discard.com',
            'mobile': '0433333333',
            'home_phone': '++9571664',
            'requested_delivery_date': timezone.now()
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_checkout_form_invalid(self):
        form = CheckoutForm(data={
            'first_name': 'First'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)

    def test_contact_form_valid_with_response_required(self):

        form = ContactForm(data={
            'type': self.contact_type,
            'title': 'Title',
            'message': 'Message',
            'preferred_contact': 'EMAIL',
            'response_required': True,
            'email': 'test@discard.com',
            'mobile': '0418333333',
            'home_phone': '0290876541',
            'rating': 3
        })
        self.assertTrue(form.is_valid())

    def test_contact_form_valid_without_response_required(self):

        form = ContactForm(data={
            'type': self.contact_type,
            'title': 'Title',
            'message': 'Message',
            'preferred_contact': 'EMAIL',
            'response_required': False,
            'rating': 3
        })
        self.assertTrue(form.is_valid())

    def test_contact_form_valid_without_rating(self):

        feedback_contact_type = ContactType.objects.create(
            id=2,
            type='FEEDBACK',
            description='description'
        )

        form = ContactForm(data={
            'type': feedback_contact_type,
            'title': 'Title',
            'message': 'Message',
            'preferred_contact': 'EMAIL',
            'response_required': False,
        })
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid_rating(self):

        form = ContactForm(data={
            'type': self.contact_type,
            'title': 'Title',
            'message': 'Message',
            'preferred_contact': 'EMAIL',
            'response_required': True,
            'email': 'test@discard.com',
            'mobile': '0418333333',
            'home_phone': '0418555555',
            'rating': 10
        })
        self.assertFalse(form.is_valid())

        # There are 2 errors in this case.
        # 1) the rating is out of range, and
        # 2) since the rating is now effectively None, its required when submitting a REVIEW contact type, hence
        # another error.
        self.assertEqual(len(form.errors), 2)

    def test_contact_form_when_response_required_invalid(self):

        form = ContactForm(data={
            'type': self.contact_type,
            'title': 'Title',
            'message': 'Message',
            'preferred_contact': 'EMAIL',
            'response_required': True,
            'rating': 1
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_contact_form_when_mobile_invalid(self):

        form = ContactForm(data={
            'type': self.contact_type,
            'title': 'Title',
            'message': 'Message',
            'preferred_contact': 'EMAIL',
            'response_required': False,
            'rating': 3,
            'mobile': '+6311111111'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_contact_form_when_home_phone_invalid(self):

        form = ContactForm(data={
            'type': self.contact_type,
            'title': 'Title',
            'message': 'Message',
            'preferred_contact': 'EMAIL',
            'response_required': False,
            'rating': 3,
            'home_phone': '+6311111111'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
