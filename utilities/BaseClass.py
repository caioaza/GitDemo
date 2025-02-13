import inspect
import logging

import pytest


from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

#from PythonSelFramework.pageObjects.HomePage import HomePage


#This class is used to hold all the common utilities, like reusable functions that need to be available for several teste cases

@pytest.mark.usefixtures("setup")
class BaseClass:


    def is_mobile_view(self):
        #Check if the current window size is mobile (width ≤ 768px)."""
        width = self.driver.get_window_size()["width"]
        return width <= 768

    def verify_link_presence(self, text):
        element = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, text)))

    def selectOptionByText(self, locator, text):
        dropdown = Select(locator)
        dropdown.select_by_visible_text(text)

    def getLogger(self):
        #this log will also generate a screenshot of the tests that failed because of the method to capture screen in conftest.py
        loggerName = inspect.stack()[1][3] #get the name of the test
        logger = logging.getLogger(loggerName)
        if not logger.handlers:  # Prevent duplicate handlers
            fileHandler = logging.FileHandler("logfile2.log", mode='a') # Append mode
            formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s :%(message)s")
            fileHandler.setFormatter(formatter)
            # Format: 2025-02-05 11:21:11,574 : WARNING : pyTests.test_logging :Something is in warning mode

            logger.addHandler(fileHandler)
            logger.setLevel(logging.DEBUG)

        logger.propagate = False #prevent duplicate logs
        return logger

    def add_three_products_to_cart(self):
        from PythonSelFramework.pageObjects.HomePage import HomePage  # Import inside the function to avoid circular imports
        homePage = HomePage(self.driver)
        checkoutpage = homePage.shopItems()
        products = checkoutpage.getProds()
        expected_cart = {}
        products_to_add = {
            "iphone X": 5,
            "Nokia Edge": 1,
            "Blackberry": 2

        }
        for product in products:
            product_title = checkoutpage.getProdTitle(product).text
            product_price = checkoutpage.getProdPrice(product).text
            if product_title in products_to_add:
                for _ in range(products_to_add[product_title]):
                    checkoutpage.getProdButton(product).click()
                expected_cart[product_title] = [products_to_add[product_title], product_price]

        return expected_cart, checkoutpage