import time
import pytest
from selenium.webdriver.common.by import By
from pageObjects.GreenKartApp.CheckOutWindow import CheckOutTab
from utilities.BaseClass import BaseClass


class GreenKartPage(BaseClass):
    """
    This class contains methods and locators for the page 'Automation Practice 1'
    """

    def __init__(self, driver):
        self.driver = driver

    pageTitle = "GreenKart - veg and fruits kart"
    greenKartLogo = (By.CSS_SELECTOR, ".brand.greenLogo")
    redLogo = (By.CLASS_NAME, "redLogo")
    searchBar = (By.CSS_SELECTOR, "input[type='search']")
    searchIcon = (By.CSS_SELECTOR, "button[type='submit']")
    products = (By.CSS_SELECTOR, "div.products")
    prodcutName = (By.CSS_SELECTOR, ".product-name")
    productQuantity = (By.CSS_SELECTOR, "input.quantity")
    addToCartButton = (By.XPATH, "//button[text()='ADD TO CART']")
    cartIcon = (By.CSS_SELECTOR, "[alt='Cart']")

    def verify_green_kart_page_is_loaded(self):
        """ Method to verify 'GREENKART' page is loaded """
        pageTitle = self.get_page_title()
        assert pageTitle == self.pageTitle
        assert self.is_element_displayed(self.greenKartLogo)
        assert self.is_element_displayed(self.redLogo)

    def enter_text_in_search_bar(self, text: str):
        """ Method to enter value in search bar on green kart home page """
        self.enter_value_in_text_field(self.searchBar, text)

    def click_on_search_icon(self):
        """ Method to click on saerch Icon """
        self.click_on_element(self.searchIcon)
        time.sleep(1)

    def search_items_in_green_kart_home_page(self, itemName: str):
        """ Method to search items in green kart home page """
        self.enter_text_in_search_bar(itemName)
        self.click_on_search_icon()

    def verify_correct_result_is_displayed_on_searching(self, itemName: str):
        self.search_items_in_green_kart_home_page(itemName)
        items = self.wait_and_find_elements(self.products)
        for item in items:
            productName = self.wait_and_find_nested_element(item, self.prodcutName, 2).text
            assert itemName in productName, f"Search item: {itemName}, Result item: {productName}"

    def click_on_add_to_cart_button(self):
        """ Merthod to click on add to cart button """
        self.click_on_element(self.addToCartButton)

    def search_and_add_item_to_cart(self, itemName: str, itemQuantity:int = 1):
        """ Method to search and add item to cart """
        self.search_items_in_green_kart_home_page(itemName)
        self.enter_value_in_text_field(self.productQuantity, itemQuantity)
        self.click_on_add_to_cart_button()
    
    def search_and_add_mulitple_items_to_cart(self, *itemDetails: tuple[dict]):
        """ Method to search and add item to cart """
        for item in itemDetails:
            self.search_items_in_green_kart_home_page(item["itemName"])
            self.enter_value_in_text_field(self.productQuantity, item["itemQuantity"])
            self.click_on_add_to_cart_button()

    def click_on_cart_icon(self):
        """ Method to click on 'Cart' icon"""
        self.click_on_element(self.cartIcon)
        checkOutTab = CheckOutTab(self.driver)
        return checkOutTab