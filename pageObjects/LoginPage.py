from selenium.webdriver.common.by import By
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass


class LoginPage(BaseClass):
    """
    This class contains methods and locators for 'Practice-project' login page
    """

    def __init__(self, driver):
        self.driver = driver

    nameField = (By.ID, "name")
    emailField = (By.ID, "email")
    submitButton = (By.ID, "form-submit")
    loadingIcon = (By.CLASS_NAME, "preloader")

    def verify_login_page_is_loaded(self):
        """ Method to verify login page is loaded """
        self.wait_for_element_to_be_invisible(self.loadingIcon)
        assert self.is_element_displayed(self.nameField)
        assert self.is_element_displayed(self.submitButton)
        assert self.is_element_displayed(self.submitButton)

    def enter_text_in_name_textfield(self, nameValue: str):
        """ Method to enter text in name text field """
        self.enter_value_in_text_field(self.nameField, nameValue)

    def enter_text_in_email_textfield(self, emailValue: str):
        """ Method to enter text in email text field """
        self.enter_value_in_text_field(self.emailField, emailValue)

    def click_on_submit_button(self):
        """ Method to click on 'submit' button """
        self.click_on_element(self.submitButton)

    def login_to_application(self, nameValue: str, emailValue: str):
        """ Wrapper to login to application """
        self.verify_login_page_is_loaded()
        self.enter_text_in_name_textfield(nameValue)
        self.enter_text_in_email_textfield(emailValue)
        self.click_on_submit_button()
        homePage = HomePage(self.driver)
        return homePage
