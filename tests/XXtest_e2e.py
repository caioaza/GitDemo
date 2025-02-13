from selenium import webdriver
import pytest

from selenium.webdriver.common.by import By


from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass


#🚀 Summary: Why Keep Locators Inside Classes and each page having its own file/class?
#✅ Clean Code → Test scripts focus on logic and calling methods only, not element-finding.
#✅ Easier Maintenance → Change locators in one place, not everywhere.
#✅ Reusability → Methods can be used in multiple tests.
#✅ Modular & Scalable → Encourages Page Object Model (POM).
#✅ Better Debugging → Errors are isolated to CheckOutPage, not test cases.
#This is why most professional automation frameworks follow this structure.

#@pytest.mark.usefixtures("setup")
class TestOne(BaseClass):

    def test_e2e(self):
        log = self.getLogger()
        homePage = HomePage(self.driver)
        checkOutPage = homePage.shopItems() #calling this method is making it click in the chekcout button and also already creates the checkoutpage object
        #confirmPage = ConfirmPage(self.driver)
        products = checkOutPage.getProds()

        for product in products:
            product_title = checkOutPage.getProdTitle(product).text
            log.info(product_title)
            if product_title == "Blackberry":
                checkOutPage.getProdButton(product).click()

        confirmPage = checkOutPage.checkOutItems() #calling the method is returning a click and also the creation of the object confirmPage
        checkOutPage.checkOutConfirm().click()
        confirmPage.sendcountry().send_keys("Ind")
        self.verify_link_presence("India")
        confirmPage.selectcountry().click()
        confirmPage.acceptterm().click()
        confirmPage.confirmOrder().click()
        successMsg = confirmPage.getMessage().text
        log.info(successMsg)

        assert("Success" in successMsg)