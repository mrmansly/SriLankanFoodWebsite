
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from ..main.acknowledgement_of_country.acknowledgement_of_country_locators import AcknowledgementOfCountryLocators
from ..main.testing_utils import get_web_driver


class SriLankanDelightsTestCase(StaticLiveServerTestCase):

    def setUp(self):

        self.browser = get_web_driver()
        self.browser.get(self.live_server_url)
        self.browser.set_page_load_timeout(10)
        self.browser.implicitly_wait(10)

        # the display of this modal is governed by a local storage flag that is not retained for each test,
        # so explicitly close the modal and continue with the rest of the test.
        self.close_acknowledgement_of_country()

    def close_acknowledgement_of_country(self):
        element = self.browser.find_element(By.ID, AcknowledgementOfCountryLocators.CLOSE_BUTTON_ID)
        # Use JavaScript to click the button to avoid being intercepted by the modal
        self.browser.execute_script("arguments[0].click();", element)

    def tearDown(self):
        if self.browser:
            try:
                self.browser.quit()
            except BrokenPipeError as p:
                print(f"Broken Pipe error during tearDown: {p}")
            except Exception as e:
                print(f"Error during tearDown: {e}")

