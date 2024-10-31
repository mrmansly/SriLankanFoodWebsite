from django.utils import timezone
from django.test import TestCase
from unittest.mock import patch
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from datetime import timedelta

from main.models import (User, Classification, Product, Cart, CartItem, Order,
                         FaqCategory, Faq, OrderProduct, ContactType, Contact,
                         SystemPreference, ProductStock, EmailConfiguration)


class TestModels(TestCase):

    def setUp(self):
        self.classification1 = Classification.objects.create(
            name='classification1',
            description='classification1 description'
        )

        self.user1 = User.objects.create(
            user_name='user1',
            password='password',
            first_name='first',
            last_name='last',
            email='email'
        )

        self.cart1 = Cart.objects.create(
            session_id='abc'
        )

        self.product1 = Product.objects.create(
            name='product1',
            description='description',
            price=10.4,
            classification=self.classification1
        )

        self.product1Stock = ProductStock.objects.create(
            product=self.product1,
            quantity=1
        )

        self.order1 = Order.objects.create(
            first_name='First',
            last_name='Last',
            email='email@email.com',
            total_price=100,
            mobile='0418502729',
            requested_delivery_date=timezone.now() + timedelta(days=1)
        )

        self.contact_type1 = ContactType.objects.create(
            type='type',
            description='description'
        )

        self.faq_category1 = FaqCategory.objects.create(
            category='category1',
            description='description1'
        )

        self.faq = Faq.objects.create(
            question='question',
            answer='answer',
            category=self.faq_category1
        )

        self.system_preference = SystemPreference.objects.create(
            name="preferenceName",
            type="boolean",
            value="True"
        )

        self.email_configuration = EmailConfiguration.objects.create(
            type='emailConfigurationType',
            from_email='fromemail@discard.com'
        )

    def test_user_unique_user_name(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                user_name='user1',
                password='password',
                first_name='first',
                last_name='last',
                email='email'
            )

    def test_product_unique_name(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name='product1',
                description='description 2',
                price=10.55,
                classification=self.classification1
            )

    def test_cart_with_user(self):
        Cart.objects.create(
            user=self.user1
        )

    def test_cart_with_non_existing_user(self):
        user = User(
            user_name='user2',
            password='password',
            first_name='first',
            last_name='last',
            email='email'
        )

        # user doesn't exist, hence FK constraint is broken
        with self.assertRaises(ValueError):
            Cart.objects.create(
                user=user
            )

    def test_cart_with_no_data(self):
        with self.assertRaises(ValueError):
            Cart.objects.create()

    def test_cart_save_with_existing_session_id(self):
        with self.assertRaises(ValidationError):
            Cart.objects.create(
                session_id='abc'
            )

    def test_cart_save_with_existing_user(self):
        Cart.objects.create(user=self.user1)

        with self.assertRaises(ValidationError):
            Cart.objects.create(user=self.user1)

    def test_cart_clean_with_no_user_or_session_id(self):
        cart = Cart()
        with self.assertRaises(ValueError):
            cart.clean()

    def test_cart_clean_with_no_user(self):
        cart = Cart(session_id="new session")
        cart.clean()

    def test_cart_clean_with_no_session(self):
        cart = Cart(user=self.user1)
        cart.clean()

    @patch('main.models.Cart.full_clean')
    def test_cart_save_with_error(self, mock_full_clean):
        cart = Cart()
        mock_full_clean.side_effect = ValueError('error')

        with self.assertRaises(ValueError):
            cart.save()

    @patch('main.models.Cart.full_clean')
    def test_cart_save_without_error(self, mock_full_clean):
        cart = Cart()
        mock_full_clean.side_effect = None
        cart.save()

    def test_cart_item_valid_save(self):
        CartItem.objects.create(
            cart=self.cart1,
            product=self.product1,
            quantity=1,
            instructions='instructions'
        )

    def test_cart_item_missing_product(self):
        with self.assertRaises(IntegrityError):
            CartItem.objects.create(
                cart=self.cart1,
                quantity=1,
                instructions='instructions'
            )

    def test_cart_item_missing_cart(self):
        with self.assertRaises(IntegrityError):
            CartItem.objects.create(
                product=self.product1,
                quantity=1,
                instructions='instructions'
            )

    def test_order_product_save(self):
        OrderProduct.objects.create(
            order=self.order1,
            product=self.product1,
            quantity=1
        )

    def test_order_product_missing_order(self):
        with self.assertRaises(IntegrityError):
            OrderProduct.objects.create(
                product=self.product1,
                quantity=1
            )

    def test_order_product_missing_product(self):
        with self.assertRaises(IntegrityError):
            OrderProduct.objects.create(
                order=self.order1,
                quantity=1
            )

    def test_contact_type_unique_type(self):
        with self.assertRaises(IntegrityError):
            ContactType.objects.create(
                type='type',
                description='description'
            )

    def test_contact_save(self):
        contact = Contact.objects.create(
            type=self.contact_type1,
            title='title',
            message='message',
            rating=1
        )
        product2 = Product.objects.create(
            name='product2',
            description='description',
            price=10.4,
            classification=self.classification1
        )

        contact.products.add(self.product1)
        contact.products.add(product2)

        # Assert
        contact = Contact.objects.get(title='title')
        self.assertEqual(contact.products.all().count(), 2)

    def test_contact_with_invalid_preferred_contact(self):
        with self.assertRaises(ValidationError):
            Contact.objects.create(
                type=self.contact_type1,
                title='title',
                message='message',
                rating=1,
                preferred_contact='invalidChoice'
            )

    def test_contact_with_invalid_type(self):
        with self.assertRaises(ValidationError):
            Contact.objects.create(
                title='title',
                message='message',
                rating=1,
            )

    def test_contact_with_invalid_rating(self):
        with self.assertRaises(ValidationError):
            Contact.objects.create(
                type=self.contact_type1,
                title='title',
                message='message',
                rating=10,
            )

    def test_contact_clean_when_valid(self):
        contact = Contact(
            type=self.contact_type1,
            title='title',
            message='message',
            rating=1,
            response_required=True,
            preferred_contact='EMAIL',
            email='email@discard.com'
        )

        contact.clean()

    def test_contact_clean_when_response_required_and_no_preferred_email(self):
        contact = Contact(
            type=self.contact_type1,
            title='title',
            message='message',
            rating=1,
            response_required=True,
            preferred_contact='EMAIL',
            email=None
        )

        with self.assertRaises(ValidationError):
            contact.clean()

    def test_contact_clean_when_response_required_and_no_preferred_mobile(self):
        contact = Contact(
            type=self.contact_type1,
            title='title',
            message='message',
            rating=1,
            response_required=True,
            preferred_contact='MOBILE',
            mobile=None
        )

        with self.assertRaises(ValidationError):
            contact.clean()

    def test_contact_clean_when_response_required_and_no_preferred_home_phone(self):
        contact = Contact(
            type=self.contact_type1,
            title='title',
            message='message',
            rating=1,
            response_required=True,
            preferred_contact='HOME_PHONE',
            home_phone=None
        )

        with self.assertRaises(ValidationError):
            contact.clean()

    @patch('main.models.Contact.full_clean')
    def test_contact_save_with_error(self, mock_full_clean):
        contact = Contact(
            type=self.contact_type1,
            title='title',
            message='message',
            rating=1,
        )
        mock_full_clean.side_effect = ValidationError('error')

        with self.assertRaises(ValidationError):
            contact.save()

    @patch('main.models.Cart.full_clean')
    def test_contact_save_without_error(self, mock_full_clean):
        contact = Contact(
            type=self.contact_type1,
            title='title',
            message='message',
            rating=1,
        )
        mock_full_clean.side_effect = None
        contact.save()

    def test_faq_category(self):
        faq_category = FaqCategory.objects.get(category='category1')
        self.assertEqual(faq_category.active, True)
        self.assertEqual(faq_category.order, 1)

    def test_faq_category_unique_category(self):
        with self.assertRaises(IntegrityError):
            FaqCategory.objects.create(
                category='category1',
                description='description2'
            )

    def test_faq_unique_question_violated(self):
        with self.assertRaises(IntegrityError):
            Faq.objects.create(
                question='question',
                answer='answer',
                category=self.faq_category1
            )

    def test_system_preference(self):
        system_preference = SystemPreference.objects.get(name="preferenceName")
        self.assertEqual(system_preference.value, 'True')
        self.assertEqual(system_preference.type, 'boolean')

    def test_system_preference_unique_name(self):
        with self.assertRaises(IntegrityError):
            SystemPreference.objects.create(name="preferenceName",
                                            type="string",
                                            value="anything")

    def test_product_stock(self):
        product_stock = ProductStock.objects.get(product_id=self.product1.id)
        self.assertEqual(product_stock.quantity, self.product1Stock.quantity)

    def test_product_stock_duplicate(self):
        with self.assertRaises(IntegrityError):
            ProductStock.objects.create(product_id=self.product1.id, quantity=1)

    def test_order_with_past_date(self):
        with self.assertRaises(ValidationError):
            Order.objects.create(
                first_name='First',
                last_name='Last',
                email='email@email.com',
                total_price=100,
                mobile='0418502729',
                requested_delivery_date=timezone.now() + timedelta(days=-10)
            )

    def test_email_configuration(self):
        email_configuration = EmailConfiguration.objects.get(type=self.email_configuration.type)
        self.assertEqual(email_configuration.from_email, self.email_configuration.from_email)

    def test_email_configuration_duplicate(self):
        with self.assertRaises(IntegrityError):
            EmailConfiguration.objects.create(type=self.email_configuration.type, from_email="anotheremail@discard.com")
