from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .acknowledgement_of_country_locators import AcknowledgementOfCountryLocators as Locators
from ..base_page.base_page_locators import BasePageLocators
from ..menu_page.menu_page_assertions import MenuPageAssertions
from ..testing_utils import get_web_driver


# Test the acknowledgement of country banner that pops up for the first time you enter this website.
# Navigating to another page blocks the acknowledgement of country banner from displaying again due to storing a
# flag in local storage when banner is closed. If cache is cleaned then the acknowledgement banner will again pop up.
class TestAcknowledgementOfCountryModal(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = get_web_driver()
        self.browser.get(self.live_server_url)
        self.browser.set_page_load_timeout(10)
        self.browser.implicitly_wait(10)

    def tearDown(self):
        if self.browser:
            try:
                self.browser.quit()
            except BrokenPipeError as p:
                print(f"Broken Pipe error during tearDown: {p}")
            except Exception as e:
                print(f"Error during tearDown: {e}")

    def test_acknowledgement_of_country_displays_first_load(self):

        # Initial load of website should display acknowledgement of country popup
        element = self.browser.find_element(By.ID, Locators.MODAL_ID)
        self.assertTrue(element.is_displayed())

    def test_close_acknowledgement_of_country_using_close_button(self):

        # click close button on acknowledgement of country modal
        element = self.browser.find_element(By.ID, Locators.CLOSE_BUTTON_ID)
        # Use JavaScript to click the button to avoid being intercepted by the modal
        self.browser.execute_script("arguments[0].click();", element)

        modal_element = self.browser.find_element(By.ID, Locators.MODAL_ID)
        self.assertFalse(modal_element.is_displayed())

    def test_close_acknowledgement_of_country_displays_only_once(self):

        # click close button on acknowledgement of country modal
        element = self.browser.find_element(By.ID, Locators.CLOSE_BUTTON_ID)
        # Use JavaScript to click the button
        self.browser.execute_script("arguments[0].click();", element)

        modal_element = self.browser.find_element(By.ID, Locators.MODAL_ID)
        self.assertFalse(modal_element.is_displayed())

        # now navigate to another page
        menu_nav_element = self.browser.find_element(By.ID, BasePageLocators.SIDENAV_MENU_ID)
        menu_nav_element.click()

        # verify that the new page has loaded
        self.assertEqual(self.browser.title, MenuPageAssertions.TITLE)

        # and the acknowledgement of country modal remains invisible.
        modal_element = self.browser.find_element(By.ID, Locators.MODAL_ID)
        self.assertFalse(modal_element.is_displayed())

    def test_close_acknowledgement_of_country_clicking_outside_of_modal(self):

        # click outside of acknowledgement modal, which should also close the modal and get to the main page.
        outside_modal_element = self.browser.find_element(By.TAG_NAME, BasePageLocators.BODY_TAG)
        # Use JavaScript to click the button
        self.browser.execute_script("arguments[0].click();", outside_modal_element)

        modal_element = self.browser.find_element(By.ID, Locators.MODAL_ID)
        self.assertFalse(modal_element.is_displayed())

    def test_close_acknowledgement_of_country_by_clicking_inside_of_modal(self):

        # clicking within the modal itself should be ignored and modal stays visible.
        element = self.browser.find_element(By.ID, Locators.TITLE_ID)
        element.click()

        modal_element = self.browser.find_element(By.ID, Locators.MODAL_ID)
        self.assertTrue(modal_element.is_displayed())