import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.headless = False  # Set to True for headless mode if desired
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()