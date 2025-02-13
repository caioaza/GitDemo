#Each page has its own class and the classes have the objects from that page. that's used instead of having the objects in the test pages

from selenium.webdriver.common.by import By

from PythonSelFramework.pageObjects.CheckoutPage import CheckOutPage


class HomePage:

    #this is the constructor
    def __init__(self,driverP): #this driver is being passed by the test_e2e page
        self.driver = driverP

    shop = (By.CSS_SELECTOR, "a[href*='shop']") #page object shop is a tuple (unmutable list)
    name = (By.CSS_SELECTOR, "input[name='name']")
    email = (By.NAME, "email")
    password = (By.ID, "exampleInputPassword1")
    checkbox = (By.ID, "exampleCheck1")
    submit = (By.XPATH, "//input[@type='submit']")
    message = (By.CLASS_NAME, "alert-success")
    gender = (By.ID, "exampleFormControlSelect1")

    def shopItems(self):
        # using the name of the class because it's a class variable. The * is to serialise (make it read as) the tuple shop and insert it in the right way
        self.driver.find_element(*HomePage.shop).click()
        obj_checkoutpage = CheckOutPage(self.driver) #creating the object for the next page here instead of creating this object in the test page
        return obj_checkoutpage

    def getName(self):
        return self.driver.find_element(*HomePage.name)

    def getEmail(self):
        return self.driver.find_element(*HomePage.email)

    def getPassword(self):
        return self.driver.find_element(*HomePage.password)

    def getCheckbox(self):
        return self.driver.find_element(*HomePage.checkbox)

    def getSubmit(self):
        return self.driver.find_element(*HomePage.submit)

    def getMessage(self):
        return self.driver.find_element(*HomePage.message)

    def getGender(self):
        return self.driver.find_element(*HomePage.gender)
