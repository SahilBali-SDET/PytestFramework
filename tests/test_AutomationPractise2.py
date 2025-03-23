import pytest
from Resources.PropertyLoader import PropertyLoader
from TestData.HomePageData import HomePageData
from pageObjects.AutomatoinPracticePage.AutomationPracticePage import PracticePage
from pageObjects.AutomatoinPracticePage.QAClickAcademyPage import QAClickAcademyPage
from pageObjects.GreenKartApp.ConfirmPage import ConfirmPage
from pageObjects.GreenKartApp.GreenKartPage import GreenKartPage
from pageObjects.GreenKartApp.CheckOutWindow import CheckOutTab
from pageObjects.HomePage import HomePage
from pageObjects.LoginPage import LoginPage
from utilities.BaseClass import BaseClass

USERNAME = PropertyLoader.get_user_name()
EMAIL = PropertyLoader.get_user_email()

@pytest.fixture(scope="class")
def setup_class(request):
    loginPage = LoginPage(request.cls.driver)
    homePage = HomePage(request.cls.driver)
    loginPage.login_to_application(USERNAME, EMAIL)
    homePage.verify_home_page_is_loaded()
    practicePage = homePage.click_on_automation_practise2_link()
    practicePage.verify_practice_page_is_loaded()
    global PRACTICE_PAGE_PAGE_URL
    PRACTICE_PAGE_PAGE_URL = practicePage.get_current_url()


@pytest.mark.usefixtures("setup_class")
class Test_HandleAlert(BaseClass):

    def teardown_method(self, method):
        practicePage = PracticePage(self.driver)

        try:
            self.accept_alert()
        except Exception:
            self.navigate_to_url(PRACTICE_PAGE_PAGE_URL)
            practicePage.verify_practice_page_is_loaded()

    def test_VerifyHandleTextIfAlertButtonIsClicked(self):
        practicePage = PracticePage(self.driver)
        alertText = "Sahil Bali - Alert"

        practicePage.enter_text_in_alret_box(alertText)
        practicePage.click_on_alert_button()
        practicePage.verify_correct_alert_text_is_displayed(alertText)
        # practicePage.dismiss_alert()
        practicePage.accept_alert() # Both works

    def test_VerifyHandleTextIfConfirmButtonIsClicked(self):
        practicePage = PracticePage(self.driver)
        alertText = "Sahil Bali - Confirm"

        practicePage.enter_text_in_alret_box(alertText)
        practicePage.click_on_confirm_button()
        practicePage.verify_correct_alert_confirm_text_is_displayed(alertText)
        practicePage.dismiss_alert()
        # practicePage.accept_alert() # Both works

    # Explicit Fail Script
    def test_VerifyHandleTextIfIncorrectButtonIsClicked(self):
        practicePage = PracticePage(self.driver)
        alertText = "Sahil Bali - Confirm"

        practicePage.enter_text_in_alret_box(alertText)
        practicePage.click_on_confirm_button()
        practicePage.verify_correct_alert_text_is_displayed(alertText)
        practicePage.accept_alert()

@pytest.mark.usefixtures("setup_class")
class Test_HandleWindows(BaseClass):

    def teardown_method(self, method):
        practicePage = PracticePage(self.driver)

        self.navigate_to_url(PRACTICE_PAGE_PAGE_URL)
        practicePage.verify_practice_page_is_loaded()

    def test_VerifyQAClickAcademyPageIsLoaded(self):
        practicePage = PracticePage(self.driver)
        qaClickAcademyPage = QAClickAcademyPage(self.driver)

        practicePage.verify_switch_window_handle_legend_is_displayed()
        practicePage.click_on_open_window_button()
        practicePage.switch_to_new_window()
        qaClickAcademyPage.veirfy_qa_click_academy_page_is_loaded()
        qaClickAcademyPage.close_current_window()
        practicePage.verify_practice_page_is_loaded()

    def test_VerifyQAClickAcademyPageIsLoadedUsingTitle(self):
        practicePage = PracticePage(self.driver)
        qaClickAcademyPage = QAClickAcademyPage(self.driver)

        practicePage.verify_switch_window_handle_legend_is_displayed()
        practicePage.click_on_open_window_button()
        practicePage.switch_to_window_by_title(qaClickAcademyPage.pageTitle)
        qaClickAcademyPage.veirfy_qa_click_academy_page_is_loaded()
        qaClickAcademyPage.close_current_window()
        practicePage.verify_practice_page_is_loaded()

@pytest.mark.usefixtures("setup_class")
class Test_HandleTabs(BaseClass):

    def teardown_method(self, method):
        practicePage = PracticePage(self.driver)

        self.navigate_to_url(PRACTICE_PAGE_PAGE_URL)
        practicePage.verify_practice_page_is_loaded()

    def test_VerifyQAClickAcademyPageIsLoaded(self):
        practicePage = PracticePage(self.driver)
        qaClickAcademyPage = QAClickAcademyPage(self.driver)

        practicePage.verify_switch_tab_legend_is_displayed()
        practicePage.click_on_open_tab_button()
        practicePage.switch_to_new_tab()
        qaClickAcademyPage.veirfy_qa_click_academy_page_is_loaded()
        qaClickAcademyPage.close_current_tab()
        practicePage.verify_practice_page_is_loaded()

    def test_VerifyQAClickAcademyPageIsLoadedUsingTitle(self):
        practicePage = PracticePage(self.driver)
        qaClickAcademyPage = QAClickAcademyPage(self.driver)

        practicePage.verify_switch_tab_legend_is_displayed()
        practicePage.click_on_open_tab_button()
        practicePage.switch_to_tab_by_title(qaClickAcademyPage.pageTitle)
        qaClickAcademyPage.veirfy_qa_click_academy_page_is_loaded()
        qaClickAcademyPage.close_current_tab()
        practicePage.verify_practice_page_is_loaded()

@pytest.mark.usefixtures("setup_class")
class Test_HandleFrame(BaseClass):

    def teardown_method(self, method):
        practicePage = PracticePage(self.driver)

        self.navigate_to_url(PRACTICE_PAGE_PAGE_URL)
        practicePage.verify_practice_page_is_loaded()

    def test_VerifyFrameIfSwitchedUsingLocator(self):
        practicePage = PracticePage(self.driver)

        practicePage.verify_frame_is_displayed()
        practicePage.switch_to_rahul_shetty_academy_frame_by_locator()
        practicePage.verify_rahul_shetty_academy_course_page_is_correcly_displayed()
        practicePage.switch_to_default_content()

    def test_VerifyFrameIfSwitchedUsingName(self):
        practicePage = PracticePage(self.driver)

        practicePage.verify_frame_is_displayed()
        practicePage.switch_to_rahul_shetty_academy_frame_by_name()
        practicePage.verify_rahul_shetty_academy_course_page_is_correcly_displayed()
        practicePage.switch_to_default_content()

    def test_VerifyFrameIfSwitchedUsingFirstFrameMethod(self):
        practicePage = PracticePage(self.driver)

        practicePage.verify_frame_is_displayed()
        practicePage.switch_to_frame()
        practicePage.verify_rahul_shetty_academy_course_page_is_correcly_displayed()
        practicePage.switch_to_default_content()

@pytest.mark.usefixtures("setup_class")
class Test_ActionChains(BaseClass):

    def test_VerifyDropdownIsDisplayedOnHoveringOverButton(self):
        practicePage = PracticePage(self.driver)

        practicePage.verify_mouser_hover_legend_is_displayed()
        practicePage.hover_over_mouse_hover_button()
        practicePage.verify_mouse_hover_dropdown_is_displayed()

    def test_VerifyDropdownOptionsAreCorrect(self):
        practicePage = PracticePage(self.driver)

        practicePage.verify_mouse_hover_dropdown_options_are_correct()

@pytest.mark.usefixtures("setup_class")
class Test_FixedTable(BaseClass):

    def test_VerifyLastRowIsDisplayed(self):
        practicePage = PracticePage(self.driver)

        practicePage.scroll_fixed_table()
        practicePage.verify_last_table_row_is_displayed()
