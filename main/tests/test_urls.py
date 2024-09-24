from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import index_view, products_view, checkout_view, about_view, \
    order_view, faq_view, contact_view, api_gateway_view, contact_submitted_view


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, index_view)

    def test_products_url_resolves(self):
        url = reverse('products')
        self.assertEqual(resolve(url).func, products_view)

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
        url = reverse('api_gateway', args=['api-path'])
        self.assertEqual(resolve(url).func, api_gateway_view)

    def test_contact_submitted_url_resolves(self):
        url = reverse('contact_submitted', args=['contact-type'])
        self.assertEqual(resolve(url).func, contact_submitted_view)
