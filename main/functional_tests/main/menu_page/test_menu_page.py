import time

from ..sri_lankan_delights_test_case import SriLankanDelightsTestCase

from django.urls import reverse
from selenium.webdriver.common.by import By
from ..base_page.base_page_locators import BasePageLocators
from main.fixtures.fixture_loader_utils import load_sample_product
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestMenuPage(SriLankanDelightsTestCase):

    def setUp(self):
        super().setUp()
        load_sample_product()
        url = self.live_server_url + reverse('menu')
        self.browser.get(url)

    def test_add_product(self):

        # add cart item by clicking the + icon
        add_qty_button = WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'add-quantity'))
        )

        add_qty_button.click()

        # verify that the cart has added one item
        cart_checkout_element = WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, BasePageLocators.CART_ITEM_CHECKOUT_ID))
        )

        self.assertTrue(cart_checkout_element.is_displayed())

        cart_items = cart_checkout_element.find_element(By.ID, BasePageLocators.CART_ITEMS_ID)
        self.assertEqual(int(cart_items.text), 1)

        # add another cart item to verify
        add_qty_button.click()

        time.sleep(0.5)

        self.assertEqual(int(cart_items.text), 2)

