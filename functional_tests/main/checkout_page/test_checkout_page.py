from ..sri_lankan_delights_test_case import SriLankanDelightsTestCase
from django.urls import reverse
from ..menu_loader_utils import load_sample_product
from selenium.webdriver.common.by import By
from .checkout_page_locators import CheckoutPageLocators


class TestCheckoutPage(SriLankanDelightsTestCase):

    def create_dummy_order(self):
        load_sample_product()
        url = self.live_server_url + reverse('menu')
        self.browser.get(url)

        # add cart item by clicking the + icon
        add_qty_button = self.browser.find_element(By.CLASS_NAME, CheckoutPageLocators.ADD_QUANTITY_CLASSNAME)
        add_qty_button.click()

    def setUp(self):
        super().setUp()
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

        delivery_date = self.browser.find_element(By.NAME, CheckoutPageLocators.FORM_REQUESTED_DELIVERY_DATE)
        self.browser.execute_script("arguments[0].value = '2024-10-12T14:22';", delivery_date)

    def test_confirm_order_on_checkout(self):

        self.add_complete_checkout_details()

        confirm_order_button = self.browser.find_element(By.ID, CheckoutPageLocators.CONFIRM_ORDER_BUTTON_ID)
        confirm_order_button.click()

        # verify that after confirming the order that the edit functions are now invisible
        edit_instructions_icon = self.browser.find_elements(By.CLASS_NAME, CheckoutPageLocators.EDIT_ICON_CLASSNAME)
        self.assertTrue(len(edit_instructions_icon) == 0)

        add_quantity_icon = self.browser.find_elements(By.CLASS_NAME, CheckoutPageLocators.ADD_ICON_CLASSNAME)
        self.assertTrue(len(add_quantity_icon) == 0)

        minus_quantity_icon = self.browser.find_elements(By.CLASS_NAME, CheckoutPageLocators.MINUS_ICON_CLASSNAME)
        self.assertTrue(len(minus_quantity_icon) == 0)
