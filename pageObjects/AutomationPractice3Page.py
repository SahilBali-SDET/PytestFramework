from selenium.webdriver.common.by import By
from utilities.BaseClass import BaseClass


class AutomationPractice3(BaseClass):
    """
    This class contains methods and locators for the page 'Automation Practice 3'
    """

    def __init__(self, driver):
        self.driver = driver

    automationPractise1LinkText = (By.PARTIAL_LINK_TEXT, "seleniumPractise/")
    automationPractise2LinkText = (By.PARTIAL_LINK_TEXT, "AutomationPractice/")
    automationPractise3LinkText = (By.PARTIAL_LINK_TEXT, "angularpractice/")
    shop = (By.CSS_SELECTOR, "a[href*='shop']")
    name = (By.CSS_SELECTOR, "[name='name']")
    email = (By.NAME, "email")
    check = (By.ID, "exampleCheck1")
    gender = (By.ID, "exampleFormControlSelect1")
    submit = (By.XPATH, "//input[@value='Submit']")
    successMessage = (By.CSS_SELECTOR, "[class*='alert-success']")

