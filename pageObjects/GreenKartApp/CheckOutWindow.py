from selenium.webdriver.common.by import By
from pageObjects.GreenKartApp.ConfirmPage import ConfirmPage
from utilities.BaseClass import BaseClass


class CheckOutTab(BaseClass):

    def __init__(self, driver):
        self.driver = driver

    cartItem = (By.CSS_SELECTOR, ".cart-preview .cart-item")
    productName = (By.CSS_SELECTOR, ".product-name")
    productPrice = (By.CSS_SELECTOR, ".product-price")
    productQuantity = (By.CSS_SELECTOR, ".quantity")
    productAmount = (By.CSS_SELECTOR, ".amount")
    productRemoveIcon = (By.CSS_SELECTOR, ".product-remove")
    proceedToCheckoutButton = (By.XPATH, "//button[text()='PROCEED TO CHECKOUT']")

    def get_all_added_items(self):
        """ Method to get all cart items """
        return self.wait_and_find_elements(self.cartItem)
    
    def click_on_proceed_to_check_out_button(self):
        """ Method to click on 'PROCEED TO CHECKOUT' button """
        self.click_on_element(CheckOutTab.proceedToCheckoutButton)
        confirm_page = ConfirmPage(self.driver)
        return confirm_page
    
    def verify_product_details_in_cart(self, *productDetails: tuple[dict]):
        """ Method to verify product details """
        allItems = self.get_all_added_items()
        expectedProductItems = [item.keys() for item in productDetails]
        assert len(allItems) == len(expectedProductItems), f"Total items added in cart are {len(allItems)}, but expected is {len(expectedProductItems)}"
        for product in productDetails:
            for item in allItems:
                productName = self.wait_and_find_nested_element(item, self.productName).text
                productPrice = self.wait_and_find_nested_element(item, self.productPrice).text
                productQuantity = self.wait_and_find_nested_element(item, self.productQuantity).text
                productAmount = self.wait_and_find_nested_element(item, self.productAmount).text
            if product["productName"] in productName:
                assert productPrice == product["productPrice"], f"Expected: {product["productPrice"]}, Actual: {productPrice}"
                assert product["productQuantity"] in productQuantity, f"Expected: {product["productQuantity"]}, Actual: {productQuantity}"
                assert productAmount == product["productAmount"], f"Expected: {product["productAmount"]}, Actual: {productAmount}"
                allItems.remove(item)
            else:
                if productDetails[-1]["productName"] in productName:
                    assert False, "No such product added in cart"
            