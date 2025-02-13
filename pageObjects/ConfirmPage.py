from selenium.webdriver.common.by import By


class ConfirmPage:
    def __init__(self,driverP):
        self.driver = driverP
    country = (By.ID, "country")
    country_select = (By.LINK_TEXT, "India")
    acceptTerm = (By.XPATH, "//div[@class='checkbox checkbox-primary']")
    confirm_order = (By.XPATH, "//input[@value='Purchase']")
    successMsg = (By.CLASS_NAME, "alert-success")

    def sendcountry(self):
        return self.driver.find_element(*ConfirmPage.country)

    def selectcountry(self):
        return self.driver.find_element(*ConfirmPage.country_select)

    def acceptterm(self):
        return self.driver.find_element(*ConfirmPage.acceptTerm)

    def confirmOrder(self):
        return self.driver.find_element(*ConfirmPage.confirm_order)

    def getMessage(self):
        return self.driver.find_element(*ConfirmPage.successMsg)

