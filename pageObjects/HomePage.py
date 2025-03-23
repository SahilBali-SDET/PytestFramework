from selenium.webdriver.common.by import By
from pageObjects.GreenKartApp.GreenKartPage import GreenKartPage
from pageObjects.AutomatoinPracticePage.AutomationPracticePage import PracticePage
from pageObjects.AutomationPractice3Page import AutomationPractice3
from pageObjects.GreenKartApp.CheckOutWindow import CheckOutTab
from utilities.BaseClass import BaseClass


class HomePage(BaseClass):
    """
    This is homepage
    """

    def __init__(self, driver):
        self.driver = driver

    automationPractise1LinkText = (By.CSS_SELECTOR, "a[href*='seleniumPractise/']")
    automationPractise2LinkText = (By.CSS_SELECTOR, "a[href*='AutomationPractice/']")
    automationPractise3LinkText = (By.CSS_SELECTOR, "a[href*='angularpractice/']")
    shop = (By.CSS_SELECTOR, "a[href*='shop']")
    name = (By.CSS_SELECTOR, "[name='name']")
    email = (By.NAME, "email")
    check = (By.ID, "exampleCheck1")
    gender = (By.ID, "exampleFormControlSelect1")
    submit = (By.XPATH, "//input[@value='Submit']")
    successMessage = (By.CSS_SELECTOR, "[class*='alert-success']")
    loadingIcon = (By.CSS_SELECTOR, ".page-wrapper .preloader span")

    def verify_home_page_is_loaded(self):
        self.wait_for_element_to_be_invisible(self.loadingIcon)
        assert self.is_element_displayed(self.automationPractise1LinkText)
        assert self.is_element_displayed(self.automationPractise2LinkText)
        assert self.is_element_displayed(self.automationPractise3LinkText)

    def click_on_automation_practise1_link(self):
        """ Method to click on link 'Automation Practise 1' """
        self.click_on_element(self.automationPractise1LinkText)
        # self.click_on_element(HomePage.automationPractise1LinkText)
        greenKartPage = GreenKartPage(self.driver)
        return greenKartPage
   
    def click_on_automation_practise2_link(self):
        """ Method to click on link 'Automation Practise 2' """
        self.click_on_element(self.automationPractise2LinkText)
        automationPracticePage = PracticePage(self.driver)
        return automationPracticePage

    def click_on_automation_practise3_link(self):
        """ Method to click on link 'Automation Practise 3' """
        self.click_on_element(self.automationPractise3LinkText)
        automationPractice3Page = AutomationPractice3(self.driver)
        return automationPractice3Page

    def shopItems(self):
        self.click_on_element(HomePage.shop)
        checkOutPage = CheckOutTab(self.driver)
        return checkOutPage

    def getName(self):
        return self.wait_and_wait_and_find_element(HomePage.name)

    def getEmail(self):
        return self.wait_and_find_element(HomePage.email)

    def getGender(self):
        return self.wait_and_find_element(HomePage.gender)

    def submitForm(self):
        return self.wait_and_find_element(HomePage.submit)

    def get_success_message(self):
        return self.wait_and_find_element(HomePage.successMessage)
