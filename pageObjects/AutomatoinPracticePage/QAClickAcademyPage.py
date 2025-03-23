from selenium.webdriver.common.by import By
from utilities.BaseClass import BaseClass


class QAClickAcademyPage(BaseClass):
    """
    This class contains methods and locators for the page 'QA CLICK ACADEMY'
    """

    def __init__(self, driver):
        self.driver = driver

    pageUrl = "https://www.qaclickacademy.com/"
    pageTitle = "QAClick Academy - A Testing Academy to Learn, Earn and Shine"
    appLogo = (By.CSS_SELECTOR, ".header-logo-support [alt='Logo']")

    def veirfy_qa_click_academy_page_is_loaded(self):
        self.wait_for_url_matches(self.pageUrl)
        pageTitle = self.get_page_title()
        assert pageTitle == self.pageTitle, f"{pageTitle} != {self.pageTitle}"
        assert self.is_element_displayed(self.appLogo)
