import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass

from TestData.HomePageData import HomePageData


class TestHomePage(BaseClass):

    def test_form_submission(self, getData):
        log = self.getLogger()
        homepage = HomePage(self.driver)
        homepage.getName().send_keys(getData["firstname"])
        log.info("first name is:"+getData["firstname"])
        homepage.getEmail().send_keys(getData["lastname"])
        homepage.getPassword().send_keys('123456')
        homepage.getCheckbox().click()
        self.selectOptionByText(homepage.getGender(), getData["gender"])
        homepage.getSubmit().click()
        message = homepage.getMessage().text
        print(message)
        assert "Success" in message
        self.driver.refresh()

    @pytest.fixture(params=HomePageData.test_HomePage_data)
    def getData(self,request): #since this is inside the class self parameter is required
        return request.param



time.sleep(2)
