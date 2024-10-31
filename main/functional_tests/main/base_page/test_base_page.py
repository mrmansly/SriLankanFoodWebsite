import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base_page_locators import BasePageLocators as Locators
from django.urls import reverse
from django.test import override_settings
from ..home_page.home_page_assertions import HomePageAssertions
from ..menu_page.menu_page_assertions import MenuPageAssertions
from ..about_page.about_page_assertions import AboutPageAssertions
from ..order_page.order_page_assertions import OrderPageAssertions
from ..faq_page.faq_page_assertions import FaqPageAssertions
from ..contact_page.contact_page_assertions import ContactPageAssertions
from ..sri_lankan_delights_test_case import SriLankanDelightsTestCase, add_gst_enabled_entry


class TestBasePage(SriLankanDelightsTestCase):

    def test_no_cart_visible(self):
        # check that the cart item is not visible in the header if there are no items
        cart_checkout_element = self.browser.find_element(By.ID, Locators.CART_ITEM_CHECKOUT_ID)
        self.assertFalse(cart_checkout_element.is_displayed())

    @override_settings(TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                # Use this mocked context to avoid session specific and database dependencies
                'main.functional_tests.main.base_page.mock_context_processor.mocked_cart_context'
            ],
        }
    }])
    def test_cart_visible_when_items_exist(self):
        # check that the cart item is visible in the header if there is at least one cart item
        self.browser.get(self.live_server_url + reverse('home'))
        cart_checkout_element = self.browser.find_element(By.ID, Locators.CART_ITEM_CHECKOUT_ID)
        self.assertTrue(cart_checkout_element.is_displayed())

    # Helper method for navigation testing
    def nav_test_for(self, element_id, title_assertion):
        try:
            self.browser.get(self.live_server_url)
            element = self.browser.find_element(By.ID, element_id)
            self.browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", element)
            time.sleep(0.1)
            self.assertEqual(self.browser.title, title_assertion)
        except Exception as e:
            print("Exception is: " + str(e))
            raise e

    def test_sidenav_home_navigation(self):
        self.nav_test_for("sidenav-home", HomePageAssertions.TITLE)

    def test_sidenav_menu_navigation(self):
        self.nav_test_for("sidenav-menu", MenuPageAssertions.TITLE)

    def test_sidenav_about_navigation(self):
        self.nav_test_for("sidenav-about", AboutPageAssertions.TITLE)

    def test_sidenav_faq_navigation(self):
        self.nav_test_for("sidenav-faq", FaqPageAssertions.TITLE)

    def test_sidenav_contact_navigation(self):
        self.nav_test_for("sidenav-contact", ContactPageAssertions.TITLE)

    def test_sidenav_order_details_navigation(self):
        add_gst_enabled_entry(True)
        self.nav_test_for("sidenav-order-details", OrderPageAssertions.TITLE)

    @override_settings(TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                # Use this mocked context to avoid session specific and database dependencies
                'main.functional_tests.main.base_page.mock_context_processor.mocked_product_stock_context'
            ],
        }
    }])
    def test_sidenav_lamprais_available_navigation(self):
        self.nav_test_for(Locators.LAMPRAIS_AVAILABLE_ID, MenuPageAssertions.TITLE)

    @override_settings(TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                # Use this mocked context to avoid session specific and database dependencies
                'main.functional_tests.main.base_page.mock_context_processor.mocked_product_stock_context'
            ],
        }
    }])
    def test_title_banner_when_lamprais_available_navigation(self):
        self.browser.get(self.live_server_url)
        elements = self.browser.find_elements(By.CLASS_NAME, Locators.LAMPRAIS_BANNER_CLASSNAME)
        elements[0].click()
        self.assertEqual(self.browser.title, MenuPageAssertions.TITLE)

    def test_title_banner_when_lamprais_not_available(self):
        self.browser.get(self.live_server_url)
        elements = self.browser.find_elements(By.CLASS_NAME, Locators.LAMPRAIS_BANNER_CLASSNAME)
        self.assertEqual(len(elements), 0)

    def test_sidenav_lamprais_available_when_no_stock(self):
        self.browser.get(self.live_server_url)

        try:
            self.browser.find_element(By.ID, Locators.LAMPRAIS_AVAILABLE_ID)
            self.fail('Element found in DOM when not expected')
        except NoSuchElementException:
            pass

    def test_footer_home_navigation(self):
        self.nav_test_for("footer-home", HomePageAssertions.TITLE)

    def test_footer_menu_navigation(self):
        self.nav_test_for("footer-menu", MenuPageAssertions.TITLE)

    def test_footer_order_details_navigation(self):
        add_gst_enabled_entry(True)
        self.nav_test_for("footer-order-details", OrderPageAssertions.TITLE)

    def test_footer_about_navigation(self):
        self.nav_test_for("footer-about", AboutPageAssertions.TITLE)

    def test_footer_faq_navigation(self):
        self.nav_test_for("footer-faq", FaqPageAssertions.TITLE)

    def test_footer_contact_navigation(self):
        self.nav_test_for("footer-contact", ContactPageAssertions.TITLE)
