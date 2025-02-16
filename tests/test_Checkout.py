import json
import os
import sys
###adding
#branch usdfiudhu
import pytest
###
# Add the root directory to the path
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from PythonSelFramework.pageObjects.HomePage import HomePage
from PythonSelFramework.utilities.BaseClass import BaseClass


class TestCart(BaseClass):

    # def test_5_checkoutbutton(self):
    #     # TC5 - Verify that the "Checkout" takes to correct page
    #
    #     _, checkoutpage = self.add_three_products_to_cart()  # captura apenas a seunfda variavel do return
    #     confirmPage = checkoutpage.checkOutItems()  # calling the method is returning a click and also the creation of the object confirmPage
    #     checkoutpage.checkOutConfirm().click()
    #
    #     # Wait for confirm order button to appear
    #     WebDriverWait(self.driver, 10).until(
    #         expected_conditions.presence_of_element_located((By.XPATH, "//input[@value='Purchase']"))
    #     )
    #
    #     # DEBUGGING: Check if element exists before assertion
    #     confirm_order_element = confirmPage.confirmOrder()
    #
    #     if confirm_order_element:
    #         print(f"Confirm Order Element Found: {confirm_order_element}")
    #     else:
    #         print("Confirm Order Element NOT Found!")
    #
    #     # print(confirmPage.confirmOrder())
    #
    #     assert confirmPage.confirmOrder().is_displayed()

    def test_1_verify_items_data(self):
        #TC2 - Verify if the items added to the cart have the same price and name displayed in products page
        logger = self.getLogger()
        try:
            expected_cart, checkoutpage = self.add_three_products_to_cart()  # captura apenas a seunfda variavel do return
            checkoutpage.checkOutItems()  # calling the method is returning a click and also the creation of the object confirmPage
            cart_products = checkoutpage.getCheckOutProducts()[:-2]
            cart_product_dict = {}
            for cart_product in cart_products:  # exclude two last items
                item_name = checkoutpage.getCheckOutProductTitle(cart_product).text
                item_price = checkoutpage.getCheckOutProductPrice(cart_product).text
                # print(item_name)
                item_quantity = int(checkoutpage.getCheckOutProductQuantity(cart_product).get_attribute('value'))
                cart_product_dict[item_name] = [item_quantity, item_price]
            #print(cart_product_dict)
            logger.info("Verifying cart items: %s", json.dumps(cart_product_dict, indent=2))
            assert cart_product_dict == expected_cart, f"Cart items mismatch! Expected: {expected_cart}, but got: {cart_product_dict}"
            logger.info("Assertion Passed: Cart contents match expected values.")
        except AssertionError as e:
            logger.error(
                "Assertion Failed! Cart items mismatch! Expected: %s, but got: %s",
                json.dumps(expected_cart, indent=2),
                json.dumps(cart_product_dict, indent=2)
            )
            sys.stdout.flush()
            raise  # Re-raise the assertion error to ensure test failure is properly registered

    @pytest.mark.parametrize("quantity, expected_total", [(9, 9), (0, 0)])
    def test_2_verify_quantity_input(self, quantity, expected_total):
        # TC Change quantity typing number over 0 and 0
        _, checkoutpage = self.add_three_products_to_cart()
        checkoutpage.checkOutItems()
        cart_products = checkoutpage.getCheckOutProducts()
        quantity_input = checkoutpage.getCheckOutProductQuantity(cart_products[1])
        price_unit = checkoutpage.getCheckOutProductPrice(cart_products[1]).text

        quantity_input.clear()
        quantity_input.send_keys(str(quantity))

        price_total = int(checkoutpage.getCheckOutProductPriceTotal(cart_products[1]).text.replace("₹. ", ''))
        assert price_total == price_unit * expected_total

    # def test_2_a_verify_quantity_input(self):
    #     #TC Change quantity typing number over 0
    #     logger = self.getLogger()
    #     _, checkoutpage = self.add_three_products_to_cart() #captura apenas a seunfda variavel do return
    #     checkoutpage.checkOutItems()  # calling the method is returning a click and also the creation of the object confirmPage
    #
    #     cart_products = checkoutpage.getCheckOutProducts()
    #     #print(cart_products)
    #     checkoutpage.getCheckOutProductQuantity(cart_products[1]).clear()
    #     checkoutpage.getCheckOutProductQuantity(cart_products[1]).send_keys("9")
    #     price_unit = checkoutpage.getCheckOutProductPrice(cart_products[1]).text
    #     price_unit = int(price_unit.replace("₹. ", ''))
    #     price_total =  checkoutpage.getCheckOutProductPriceTotal(cart_products[1]).text
    #     price_total = int(price_total.replace("₹. ", ''))
    #     print(price_unit)
    #     print(price_total)
    #
    #     assert price_unit * 9 == price_total
    #
    # def test_2_b_verify_quantity_input(self):
    #     #Change quantity typing 0
    #
    #
    #     _, checkoutpage = self.add_three_products_to_cart() #captura apenas a seunfda variavel do return
    #     checkoutpage.checkOutItems()  # calling the method is returning a click and also the creation of the object confirmPage
    #
    #     cart_products = checkoutpage.getCheckOutProducts()
    #     # print(cart_products)
    #     checkoutpage.getCheckOutProductQuantity(cart_products[1]).clear()
    #     checkoutpage.getCheckOutProductQuantity(cart_products[1]).send_keys("0")
    #     price_total = checkoutpage.getCheckOutProductPriceTotal(cart_products[1]).text
    #     price_total = int(price_total.replace("₹. ", ''))
    #     print(price_total)
    #
    #     assert price_total == 0



    def test_6_checkout_emptycart_button(self):
        #TC6 - Verify checkout button is not displayed when cart is empty
        homePage = HomePage(self.driver)
        checkoutpage = homePage.shopItems()
        checkoutpage.checkOutItems()

        assert len(checkoutpage.getCheckOutProducts()) == 2 and not  checkoutpage.checkOutConfirm().is_displayed()

    def test_7_remove_product(self):
        #TC7 - Test removing a product from the cart.
        _, checkoutpage = self.add_three_products_to_cart() #captura apenas a seunfda variavel do return
        checkoutpage.checkOutItems()  # calling the method is returning a click and also the creation of the object confirmPage

        cart_products = checkoutpage.getCheckOutProducts()
        checkoutpage.getRemoveButton(cart_products[1]).click()
        cart_products = checkoutpage.getCheckOutProducts()
        print(len(cart_products))
        assert len(cart_products) == 4

    def test_9_verify_total(self):
        #TC9 - Verify total is correct
        _, checkoutpage = self.add_three_products_to_cart() #captura apenas a seunfda variavel do return
        checkoutpage.checkOutItems()  # calling the method is returning a click and also the creation of the object confirmPage
        cart_products = checkoutpage.getCheckOutProducts()[:-2]

        total_price_product = 0  # Initialize total sum

        for cart_product in cart_products:
            price_product_total = checkoutpage.getCheckOutProductPriceTotal(cart_product).text
            price_product_total = int(price_product_total.replace("₹. ", ''))
            total_price_product += price_product_total

        #outerHtml prints the actual html element
        #print(last_product.get_attribute("outerHTML"))

        total = checkoutpage.getCheckOutTotal().text
        total = int(total.replace("₹. ", ''))

        assert total_price_product == total

    def test_10_verify_checkout_empty_cart(self):
        _, checkoutpage = self.add_three_products_to_cart() #captura apenas a seunfda variavel do return
        assert checkoutpage.getCheckoutButton().text ==  "Checkout ( 8 )"











