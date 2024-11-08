from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views.web_views import index_view, menu_view, checkout_view, about_view, \
    order_view, faq_view, contact_view, contact_submitted_view
from main.views.api_views import CartItemQuantityUpdateView


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, index_view)

    def test_menu_url_resolves(self):
        url = reverse('menu')
        self.assertEqual(resolve(url).func, menu_view)

    def test_checkout_url_resolves(self):
        url = reverse('checkout')
        self.assertEqual(resolve(url).func, checkout_view)

    def test_about_url_resolves(self):
        url = reverse('about')
        self.assertEqual(resolve(url).func, about_view)

    def test_order_url_resolves(self):
        url = reverse('order')
        self.assertEqual(resolve(url).func, order_view)

    def test_faq_url_resolves(self):
        url = reverse('faq')
        self.assertEqual(resolve(url).func, faq_view)

    def test_contact_url_resolves(self):
        url = reverse('contact')
        self.assertEqual(resolve(url).func, contact_view)

    def test_api_gateway_url_resolves(self):
        url = reverse('update_cart_item_api')
        self.assertEqual(resolve(url).func.view_class, CartItemQuantityUpdateView)

    def test_contact_submitted_url_resolves(self):
        url = reverse('contact_submitted', args=['contact-type'])
        self.assertEqual(resolve(url).func, contact_submitted_view)
