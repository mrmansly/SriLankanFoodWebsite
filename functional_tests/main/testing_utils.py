import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions


# get the selenium web driver to use based on the DJANGO_TEST_BROWSER
# environment variable. Defaults to Chrome.
def get_web_driver():

    web_driver = None
    test_browser = os.environ.get("DJANGO_TEST_BROWSER")

    if test_browser:
        if test_browser == 'chrome':
            web_driver = get_chrome_driver()
        elif test_browser == 'firefox':
            web_driver = get_firefox_driver()
        elif test_browser == 'safari':
            web_driver = get_safari_driver
        elif test_browser == 'edge':
            web_driver = get_edge_driver()
    else:
        # default to Chrome if nothing set
        web_driver = get_chrome_driver()

    return web_driver


def get_chrome_driver():
    chrome_options = ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    service = ChromeService()
    return webdriver.Chrome(service=service, options=chrome_options)


def get_firefox_driver():
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")
    service = FirefoxService()
    return webdriver.Firefox(service=service, options=firefox_options)


# Not tested
def get_safari_driver():
    return webdriver.Safari()


def get_edge_driver():
    edge_options = EdgeOptions()
    edge_options.add_argument("--headless")
    service = EdgeService()
    return webdriver.Edge(service=service, options=edge_options)