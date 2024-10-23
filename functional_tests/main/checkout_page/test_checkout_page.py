from ..sri_lankan_delights_test_case import SriLankanDelightsTestCase
from django.urls import reverse
from ..menu_loader_utils import load_sample_product
from selenium.webdriver.common.by import By
from .checkout_page_locators import CheckoutPageLocators
from ..sri_lankan_delights_test_case import create_gst_preferences
from django.utils import timezone
from datetime import timedelta


class TestCheckoutPage(SriLankanDelightsTestCase):

    def create_dummy_order(self):
        url = self.live_server_url + reverse('menu')
        self.browser.get(url)

        # add cart item by clicking the + icon
        add_qty_button = self.browser.find_element(By.CLASS_NAME, CheckoutPageLocators.ADD_QUANTITY_CLASSNAME)
        add_qty_button.click()

    def setUp(self):
        super().setUp()
        create_gst_preferences()
        load_sample_product()
        self.create_dummy_order()
        url = self.live_server_url + reverse('checkout')
        self.browser.get(url)

    def test_edit_functions_visible(self):

        # verify that the edit instructions and edit quantity buttons are not visible.
        edit_instructions_icon = self.browser.find_element(By.CLASS_NAME, CheckoutPageLocators.EDIT_ICON_CLASSNAME)
        self.assertTrue(edit_instructions_icon.is_displayed())

        add_quantity_icon = self.browser.find_element(By.CLASS_NAME, CheckoutPageLocators.ADD_ICON_CLASSNAME)
        self.assertTrue(add_quantity_icon.is_displayed())

        minus_quantity_icon = self.browser.find_element(By.CLASS_NAME, CheckoutPageLocators.MINUS_ICON_CLASSNAME)
        self.assertTrue(minus_quantity_icon.is_displayed())

    # Helper method to add details to the checkout form
    def add_complete_checkout_details(self):

        first_name = self.browser.find_element(By.NAME, CheckoutPageLocators.FORM_FIRST_NAME)
        first_name.send_keys('Graeme')

        last_name = self.browser.find_element(By.NAME, CheckoutPageLocators.FORM_LAST_NAME)
        last_name.send_keys('Eaton')

        email = self.browser.find_element(By.NAME, CheckoutPageLocators.FORM_EMAIL)
        email.send_keys('geaton@email.com')

        mobile = self.browser.find_element(By.NAME, CheckoutPageLocators.FORM_MOBILE)
        mobile.send_keys('0418540200')

        # delivery date is defaulted with a valid current date so no date setting is required.

    def test_confirm_order_on_checkout(self):

        self.add_complete_checkout_details()

        self.confirm_order()

        # verify that after confirming the order that the edit functions are now invisible
        edit_instructions_icon = self.browser.find_elements(By.CLASS_NAME, CheckoutPageLocators.EDIT_ICON_CLASSNAME)
        self.assertTrue(len(edit_instructions_icon) == 0)

        add_quantity_icon = self.browser.find_elements(By.CLASS_NAME, CheckoutPageLocators.ADD_ICON_CLASSNAME)
        self.assertTrue(len(add_quantity_icon) == 0)

        minus_quantity_icon = self.browser.find_elements(By.CLASS_NAME, CheckoutPageLocators.MINUS_ICON_CLASSNAME)
        self.assertTrue(len(minus_quantity_icon) == 0)

    def confirm_order(self):
        confirm_order_button = self.browser.find_element(By.ID, CheckoutPageLocators.CONFIRM_ORDER_BUTTON_ID)
        confirm_order_button.click()

    def test_confirm_order_on_checkout_with_past_date(self):

        self.add_complete_checkout_details()
        delivery_date = self.browser.find_element(By.NAME, CheckoutPageLocators.FORM_REQUESTED_DELIVERY_DATE)
        date = timezone.now() + timedelta(days=-10)
        formatted_date = date.strftime('%Y-%m-%dT%H:%M')
        # '2024-10-12T14:22'
        self.browser.execute_script("arguments[0].value = '" + formatted_date + "';", delivery_date)

        self.confirm_order()

        # verify that after confirming the order that the edit functions are now invisible
        edit_instructions_icon = self.browser.find_elements(By.CLASS_NAME, CheckoutPageLocators.EDIT_ICON_CLASSNAME)
        self.assertTrue(len(edit_instructions_icon) == 1)

        add_quantity_icon = self.browser.find_elements(By.CLASS_NAME, CheckoutPageLocators.ADD_ICON_CLASSNAME)
        self.assertTrue(len(add_quantity_icon) == 1)

        minus_quantity_icon = self.browser.find_elements(By.CLASS_NAME, CheckoutPageLocators.MINUS_ICON_CLASSNAME)
        self.assertTrue(len(minus_quantity_icon) == 1)

