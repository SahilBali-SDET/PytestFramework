from selenium.webdriver.common.by import By
from utilities.BaseClass import BaseClass
from colorCode.colorCode import Colors

class ConfirmPage(BaseClass):

    def __init__(self, driver):
        self.driver = driver

    productTable = (By.CSS_SELECTOR, "table#productCartTables")
    promoCodeField = (By.CSS_SELECTOR, "input.promoCode")
    applyPromoButton = (By.CSS_SELECTOR, ".promoBtn")
    placeOrderButton = (By.XPATH, "//button[text()='Place Order']")
    # select country page
    selectCountryDropdown = (By.TAG_NAME, "select")
    agreeToTermsCheckbox = (By.CSS_SELECTOR, "[type='checkbox']")
    proceedButton = (By.XPATH, "//button[text()='Proceed']")
    # success message page
    successMessage = (By.CSS_SELECTOR, ".products span[style]")
    expectedSuccessMessage = "Thank you, your order has been placed successfully\nYou'll be redirected to Home page shortly!!"

    def verify_confirm_page_is_loaded(self):
        """ Method to veirfy confirm page is loaded """
        assert self.is_element_displayed(self.productTable)
        assert self.is_element_displayed(self.promoCodeField)
        assert self.is_element_displayed(self.applyPromoButton)
        assert self.is_element_displayed(self.placeOrderButton)

    def click_on_place_order_button(self):
        """ Method to click on 'Place Order' button """
        self.click_on_element(self.placeOrderButton)

    def wait_until_select_country_page_is_laoded(self):
        self.wait_for_element_to_be_visible(self.selectCountryDropdown)

    def select_country_from_dropdown(self, countryName: str):
        """ Method to select country from dropdown """
        self.select_option_by_text(self.selectCountryDropdown, countryName)

    def check_agree_to_terms_checkbox(self):
        """ Check 'Agrre to Terms and Conditions' checkbox """
        self.click_on_element(self.agreeToTermsCheckbox)

    def click_on_proceed_button(self):
        """ Method to click on 'Proceed' button """
        self.click_on_element(self.proceedButton)
        
    def verify_success_message_is_displayed(self):
        """ Method to verify order succesfully placed message is displayed """
        assert self.is_element_displayed(self.successMessage)
        actualSuccessText = self.get_element_text(self.successMessage)
        assert actualSuccessText == self.expectedSuccessMessage

    def verify_success_message_is_displayed_in_green_color(self):
        """ Method to verify color of success message """
        actualColor = self.get_css_property(self.successMessage, "color")
        assert actualColor == Colors.green, f"Expected color: {Colors.green}, Actual color: {actualColor}"
