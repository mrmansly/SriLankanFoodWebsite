import json
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from main.forms import CheckoutForm, ContactForm
from main.models import Cart, CartItem, Product, Classification, ContactType, \
    Faq, FaqCategory, Order, OrderProduct, ProductStock
from main.views import get_session_id, get_serialized_cart


class TestViews(TestCase):

    def setUp(self):
        # Create sample classifications and products
        self.electronics_classification = Classification.objects.create(name='Electronics', order=1)
        self.books_classification = Classification.objects.create(name='Books', order=2)

        Product.objects.create(name='Laptop', price=1000, classification=self.electronics_classification)
        self.book_product = Product.objects.create(name='Book', price=20, classification=self.books_classification)

        self.book_product_stock = ProductStock.objects.create(product=self.book_product, quantity=2)

        session = self.client.session
        session['session_key'] = 'mocked-session-id'
        session.save()

    def test_index_view_GET(self):
        url = reverse('home')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    @patch('main.views.get_cart')  # Adjust the import path to your actual view location
    @patch('main.views.get_session_id')  # Adjust the import path to your actual view location
    def test_menu_view_GET(self, mock_get_session_id, mock_get_cart):
        # Mock the session ID and cart items
        mock_get_session_id.return_value = 'mock_session_id'
        mock_cart = mock_get_cart.return_value
        mock_cart.cart_items.all.return_value = ['Item1', 'Item2']

        # Simulate a GET request to the products view
        response = self.client.get(reverse('menu'))  # Adjust the name if needed

        # Assert the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert the template used is 'main/products.html'
        self.assertTemplateUsed(response, 'main/menu.html')

        # Assert the context contains the expected data
        self.assertIn('classifications', response.context)
        self.assertIn('cartItems', response.context)

        # Assert the correct data is in the context
        self.assertEqual(len(response.context['classifications']), 2)  # 2 classifications created
        self.assertEqual(response.context['cartItems'], ['Item1', 'Item2'])


        # Assert that product stock is retrieved (where applicable)
        classifications = response.context['classifications']
        book_classification = classifications.filter(name='Books').first()
        book_product = book_classification.product_set.first()
        self.assertEqual(book_product.stock.quantity, self.book_product_stock.quantity)

        electronic_classification = classifications.filter(name='Electronics').first()
        laptop_product = electronic_classification.product_set.first()
        with self.assertRaises(mProductStock.DoesNotExist):
            _ = laptop_product.stock

        # Optionally assert that the mocked functions were called
        mock_get_session_id.assert_called_once_with(response.wsgi_request)
        mock_get_cart.assert_called_once_with('mock_session_id')

    @patch('main.views.get_cart')
    @patch('main.views.get_session_id')
    @patch('main.views.get_all_price_data')
    def test_checkout_view_GET(self, mock_get_all_price_data,
                               mock_get_session_id,
                               mock_get_cart):
        # Mock the cart and session ID
        mock_get_session_id.return_value = 'mock_session_id'
        mock_cart = mock_get_cart.return_value
        item_list = ['Item1', 'Item2']
        mock_cart.cart_items.all.return_value = item_list  # Mock cart items

        price_data = {}
        mock_get_all_price_data.return_value = price_data

        # Simulate a POST request to the checkout view
        response = self.client.get(reverse('checkout'))

        # Assert that the response is a render of the order confirmed template
        self.assertTemplateUsed(response, 'main/checkout.html')

        # Assert the context contains the expected data
        self.assertIn('item_list', response.context)
        self.assertIn('form', response.context)
        self.assertIn('update_allowed', response.context)
        self.assertIn('price_data', response.context)

        # Assert the values in the context
        self.assertIsInstance(response.context['form'], CheckoutForm)
        self.assertEqual(response.context['item_list'], item_list)
        self.assertEqual(response.context['price_data'], price_data)
        self.assertEqual(response.context['update_allowed'], True)

        # Optionally assert that the mocked functions were called
        mock_get_session_id.assert_called_once_with(response.wsgi_request)
        mock_get_cart.assert_called_once_with('mock_session_id')
        mock_get_all_price_data.assert_called_once_with(item_list)

    @patch('main.views.get_cart')
    @patch('main.views.get_session_id')
    @patch('main.views.save_checkout_form')
    @patch('main.views.get_all_price_data')
    def test_checkout_view_confirmation_valid_form(self, mock_get_all_price_data, mock_save_checkout_form,
                                                   mock_get_session_id,
                                                   mock_get_cart):
        # Create a mock order object to return
        mock_order = MagicMock(spec=Order)
        mock_order.id = 1
        mock_order.created_date = '2024-01-01'

        mock_product = MagicMock(spec=OrderProduct)
        mock_product.name = "Name"

        mock_order.order_products.all.return_value = [mock_product]

        mock_save_checkout_form.return_value = mock_order

        # Mock the cart and session ID
        mock_get_session_id.return_value = 'mock_session_id'
        mock_cart = mock_get_cart.return_value

        price_data = {}
        mock_get_all_price_data.return_value = price_data

        # mock_cart.cart_items.all.return_value = ['Item1', 'Item2']  # Mock cart items

        # Prepare valid POST data
        valid_data = {
            'form_type': 'checkout',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'mobile': '0418502729',
            'requested_delivery_date': timezone.now() + timedelta(days=2)
            # Include any other required fields for CheckoutForm
        }

        # Simulate a POST request to the checkout view
        response = self.client.post(reverse('checkout'), data=valid_data)

        # Assert that the response is a render of the order confirmed template
        self.assertTemplateUsed(response, 'main/order-confirmed.html')

        # Assert the context contains the expected data
        self.assertIn('item_list', response.context)
        self.assertIn('order_id', response.context)
        self.assertIn('order_date', response.context)
        self.assertIn('update_allowed', response.context)
        self.assertIn('price_data', response.context)

        # Assert the values in the context
        self.assertEqual(response.context['order_id'], mock_order.id)
        self.assertEqual(response.context['order_date'], mock_order.created_date)
        self.assertEqual(response.context['item_list'], mock_order.order_products.all())
        self.assertEqual(response.context['price_data'], price_data)

        # Optionally assert that the mocked functions were called
        mock_get_session_id.assert_called_once_with(response.wsgi_request)
        mock_get_cart.assert_called_once_with('mock_session_id')

        form = CheckoutForm(valid_data)
        form.is_valid()

        mock_save_checkout_form.assert_called_once()
        args, _ = mock_save_checkout_form.call_args

        self.assertIsInstance(args[0], CheckoutForm)
        self.assertEqual(args[1], mock_cart)

    @patch('main.views.get_cart')
    @patch('main.views.get_session_id')
    @patch('main.views.get_all_price_data')
    def test_checkout_view_confirmation_invalid_form(self, mock_get_all_price_data, mock_get_session_id, mock_get_cart):
        # Mock the session ID and cart
        mock_get_session_id.return_value = 'mock_session_id'
        mock_cart = mock_get_cart.return_value

        item_list = ['Item1', 'Item2']
        mock_cart.cart_items.all.return_value = item_list

        price_data = {'price': 10}
        mock_get_all_price_data.return_value = price_data

        # Prepare invalid POST data
        invalid_data = {
            'form_type': 'checkout',
            # Missing required fields
        }

        response = self.client.post(reverse('checkout'), data=invalid_data)

        # Assert that the same template is returned including the form errors
        self.assertTemplateUsed(response, 'main/checkout.html')
        self.assertEqual(response.status_code, 200)
        # Ensure form errors are present in the context
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())

        self.assertTrue(response.context['update_allowed'])
        self.assertEqual(response.context['price_data'], price_data)
        self.assertEqual(response.context['item_list'], item_list)

    def test_about_view(self):
        # Simulate a GET request to the 'about' view
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'main/about.html')
        self.assertEqual(response.status_code, 200)

    @patch('main.views.get_all_price_data')  # Mock get_all_price_data
    @patch('main.views.get_cart')  # Mock get_cart
    @patch('main.views.get_session_id')  # Mock get_session_id
    def test_order_view_get_request(self, mock_get_session_id, mock_get_cart, mock_get_all_price_data):
        # Mock the session ID
        mock_get_session_id.return_value = 'mock_session_id'

        # Mock the cart and cart items
        mock_cart = MagicMock()
        item_list = ['item1', 'item2']
        mock_cart.cart_items.all.return_value = item_list  # Mock the items in the cart
        mock_get_cart.return_value = mock_cart

        # Mock the price data
        price_data = {"total": 100}
        mock_get_all_price_data.return_value = price_data

        # Send a GET request to the order_view
        response = self.client.get(reverse('order'))

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'main/order.html')

        # Check if the response contains the expected context data
        self.assertEqual(response.context['item_list'], item_list)
        self.assertEqual(response.context['price_data'], price_data)
        self.assertTrue(response.context['update_allowed'])

        # Assert that get_session_id was called once
        mock_get_session_id.assert_called_once_with(response.wsgi_request)

        # Assert that get_cart was called with the correct session ID
        mock_get_cart.assert_called_once_with('mock_session_id')

        # Assert that get_all_price_data was called with the correct item list
        mock_get_all_price_data.assert_called_once_with(item_list)

    @patch('main.views.Faq.objects.filter')  # Mock Faq.objects.filter
    @patch('main.views.FaqCategory.objects.filter')  # Mock FaqCategory.objects.filter
    def test_faq_view_get_request(self, mock_faq_category_filter, mock_faq_filter):
        faq_category = FaqCategory(category='category')
        faq = Faq(category=faq_category)
        # Mock FAQ list and category list
        mock_faqs = [faq]  # Mock some FAQ objects
        mock_categories = [faq_category]  # Mock some FAQCategory objects

        # Configure the mock filters to return the mock lists
        mock_faq_filter.return_value = mock_faqs
        mock_faq_category_filter.return_value.order_by.return_value = mock_categories

        # Send a GET request to the FAQ view
        response = self.client.get(reverse('faq'))

        # Check that the correct template was used
        self.assertTemplateUsed(response, 'main/faq.html')

        # Check that the correct context data was passed to the template
        self.assertEqual(response.context['faqs'], mock_faqs)
        self.assertEqual(response.context['category_list'], mock_categories)

        # Ensure the filter for active FAQs was called
        mock_faq_filter.assert_called_once_with(active=True)

        # Ensure the filter for active FAQ categories was called and ordered by "order"
        mock_faq_category_filter.assert_called_once_with(active=True)
        mock_faq_category_filter.return_value.order_by.assert_called_once_with("order")

    def test_contact_view_GET(self):
        response = self.client.get(reverse('contact'))

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'main/contact.html')

        # Ensure the form is in the context
        self.assertIn('form', response.context)

        form_context = response.context['form']
        self.assertIs(form_context, ContactForm)

    @patch('main.views.save_contact')  # Mock the save_contact function
    def test_contact_view_post_valid_form(self, mock_save_contact):

        # Create an entry for form validation to be successful, hence why a rating must be passed through as well.
        ContactType.objects.create(type="REVIEW")

        # Create a mock contact object
        mock_contact = MagicMock()
        mock_contact.type.type = 'general'
        mock_save_contact.return_value = mock_contact

        # Valid form data
        post_data = {
            'type': ContactType.objects.first().id,
            'title': 'Title',
            'email': 'john@example.com',
            'message': 'This is a test message.',
            'rating': 2
        }

        response = self.client.post(reverse('contact'), data=post_data)

        # Check if save_contact was called with the valid form
        self.assertTrue(mock_save_contact.called)

        # Check if it redirects to the correct URL after saving
        self.assertRedirects(response, reverse('contact_submitted', kwargs={'contact_type': 'general'}))

    def test_contact_view_post_invalid_form(self):
        # Invalid form data (missing required fields, for example)
        post_data = {
            'message': ''  # Missing required fields
        }

        response = self.client.post(reverse('contact'), data=post_data)

        # Ensure the template is re-rendered with form errors
        self.assertTemplateUsed(response, 'main/contact.html')

        # Ensure form errors are present in the context
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())

    def test_get_session_id_existing_session(self):
        # Mock request with an existing session
        request = MagicMock()
        request.session.session_key = 'existing_session_key'

        session_id = get_session_id(request)
        self.assertEqual(session_id, 'existing_session_key')
        request.session.create.assert_not_called()  # Ensure create is not called

    def test_get_session_id_no_session(self):
        # Mock request with no existing session
        request = MagicMock()
        request.session.session_key = None
        request.session.create = MagicMock()  # Mock create method

        session_id = get_session_id(request)

        # We cannot verify the session id as we are mocking the create method. Therefore simulate the setting of the
        # session key that occurs as part of the request.session.create().
        # self.assertIsNotNone(session_id)  # Check that session_id is created
        request.session.create.assert_called_once()  # Ensure create is called

    def test_contact_submitted_view(self):
        # Arrange
        contact_type = "support"

        # Act
        response = self.client.get(reverse('contact_submitted', args=[contact_type]))

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contact-submitted.html')
        self.assertIn('contact_type', response.context)
        self.assertEqual(response.context['contact_type'], contact_type)

    @patch('main.views.add_product')
    @patch('main.views.get_serialized_cart')
    def test_api_gateway_update_cart_item_quantity(self, mock_get_serialized_cart, mock_add_product):
        # Arrange
        api_path = 'update-cart-item-quantity'
        mock_request_data = {
            'cart_id': '1',
            'product_id': 2,
            'quantity': 5,
            'instructions': 'No onions'
        }
        mock_get_serialized_cart.return_value = {
            'key': 'value'
        }

        url = reverse('api_gateway', args=[api_path])  # Replace with the actual name of your URL pattern

        # Act
        response = self.client.post(url, data=json.dumps(mock_request_data), content_type='application/json', type=json)

        # Assert
        self.assertEqual(response.status_code, 200)
        mock_add_product.assert_called_once_with(1, 2, 5, 'No onions')
        mock_get_serialized_cart.assert_called_once()
        self.assertEqual(response.data, {'key': 'value'})  # Adjust based on actual output

    def test_api_gateway_unrecognized_api_path(self):
        # Arrange
        api_path = 'unknown-path'
        url = reverse('api_gateway', args=[api_path])

        # Act
        response = self.client.post(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello from Django!'})

    @patch('main.views.get_session_id')
    def test_get_serialized_cart(self, mock_get_session_id):
        Cart.objects.create(session_id='12345')
        cart = Cart.objects.get(session_id='12345')
        CartItem.objects.create(cart=cart, product=Product.objects.get(name='Laptop'), quantity=1)

        mock_get_session_id.return_value = '12345'

        unused_request = None
        response = get_serialized_cart(unused_request)

        self.assertEqual(response['id'],1)
        self.assertEqual(response['session_id'], '12345')
        self.assertEqual(len(response['cart_items']), 1)

