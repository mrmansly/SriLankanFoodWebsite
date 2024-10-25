from ..sri_lankan_delights_test_case import SriLankanDelightsTestCase
from django.urls import reverse
from .order_page_locators import OrderPageLocators
from ..menu_page.menu_page_assertions import MenuPageAssertions
from selenium.webdriver.common.by import By
from ..sri_lankan_delights_test_case import create_gst_preferences


class TestOrderPage(SriLankanDelightsTestCase):

    def setUp(self):
        super().setUp()
        create_gst_preferences()
        url = self.live_server_url + reverse('order')
        self.browser.get(url)

    def test_empty_rice_cooker_menu_link(self):

        # if no cart items then empty rice cooker page should allow a redirect back
        # to the menu page
        element = self.browser.find_element(By.ID, OrderPageLocators.EMPTY_RICE_COOKER_MENU_LINK_ID)
        element.click()

        self.assertEqual(self.browser.title, MenuPageAssertions.TITLE)