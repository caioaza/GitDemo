from selenium.webdriver.common.by import By

from PythonSelFramework.pageObjects.ConfirmPage import ConfirmPage

from PythonSelFramework.utilities.BaseClass import BaseClass


#The test script focuses only on actions, not locators.
#The CheckOutPage class manages all locators, keeping things clean.

class CheckOutPage(BaseClass):

    def __init__(self, driverP):
        self.driver = driverP

    products = (By.XPATH, "//div[@class='card h-100']")
    product_button = (By.XPATH, ".//button[@class='btn btn-info']")
    product_title = (By.XPATH, "div/h4/a")
    product_price = (By.XPATH, "div/h5")
    checkout = (By.CSS_SELECTOR, "a[class*='btn-primary']")
    checkout_menu_button = (By.XPATH, "//button[@aria-label='Toggle navigation']") # Mobile menu button
    checkout_menu_items = (By.ID, "navbarResponsive")  # Menu items
    checkout_products = (By.XPATH, "//tbody/tr")
    checkout_product_title = (By.XPATH, "td/div/div/h4/a")
    checkout_product_price = (By.XPATH, "td[3]/strong")
    checkout_product_price_total = (By.XPATH, "td[4]/strong")
    checkout_product_quantity = (By.CSS_SELECTOR, ".form-control")
    checkout_confirmation = (By.CSS_SELECTOR, ".btn.btn-success")
    checkout_remove_item = (By.XPATH, "//button[normalize-space()='Remove']")
    checkout_total = (By.CSS_SELECTOR, "td[class='text-right'] h3 strong")

    def getProds(self):
        return self.driver.find_elements(*CheckOutPage.products)

    def getProdButton(self, product):
        return product.find_element(*CheckOutPage.product_button)

    def getCheckoutButton(self):
        return self.driver.find_element(*CheckOutPage.checkout)

    def getProdTitle(self, product):
        return product.find_element(*CheckOutPage.product_title)

    def getProdPrice(self, product):
        return product.find_element(*CheckOutPage.product_price)

    def checkOutItems(self):
        self.open_menu()
        self.driver.find_element(*CheckOutPage.checkout).click()
        confirmPage = ConfirmPage(self.driver)
        return confirmPage

    def getCheckOutProducts(self):
        return self.driver.find_elements(*CheckOutPage.checkout_products)

    def getCheckOutProductTitle(self,checkout_product):
        return checkout_product.find_element(*CheckOutPage.checkout_product_title)

    def getCheckOutProductPrice(self,checkout_product):
        return checkout_product.find_element(*CheckOutPage.checkout_product_price)

    def getCheckOutProductPriceTotal(self, checkout_product):
        return checkout_product.find_element(*CheckOutPage.checkout_product_price_total)

    def getCheckOutProductQuantity(self,checkout_product):
        return checkout_product.find_element(*CheckOutPage.checkout_product_quantity)

    def checkOutConfirm(self):
        return self.driver.find_element(*CheckOutPage.checkout_confirmation)

    def getRemoveButton(self,checkout_product):
        return checkout_product.find_element(*CheckOutPage.checkout_remove_item)

    def getCheckOutTotal(self):
        return self.driver.find_element(*CheckOutPage.checkout_total)

    def open_menu(self):
        if self.is_mobile_view():
            return self.driver.find_element(*CheckOutPage.checkout_menu_button).click()  # Click only if on mobile

    def is_menu_visible(self):
        #Checks if menu items are visible"""
        return self.driver.find_element(*CheckOutPage.checkout_menu_items).is_displayed()



