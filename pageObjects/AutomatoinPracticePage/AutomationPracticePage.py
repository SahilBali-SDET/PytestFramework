import time
from selenium.webdriver.common.by import By
from utilities.BaseClass import BaseClass


class PracticePage(BaseClass):
    """
    This class contains methods and locators for the page 'Automation Practice 2'
    """

    def __init__(self, driver):
        self.driver = driver

    pageUrl = "https://rahulshettyacademy.com/AutomationPractice/"
    pageTitle = "Practice Page"
    appLogo = (By.CSS_SELECTOR, "a .logoClass")

    # Alert
    alertTextField = (By.ID, "name")
    alretButton = (By.ID, "alertbtn")
    confirmButton = (By.ID, "confirmbtn")
    alertText = "Hello {}, share this practice page and share your knowledge"
    alertConfirmText = "Hello {}, Are you sure you want to confirm?"

    # windows
    switchWindowLegend = (By.XPATH, "//legend[text()='Switch Window Example']")
    openWindowButton = (By.ID, "openwindow")

    # tabs
    switchTabLegend = (By.XPATH, "//legend[text()='Switch Tab Example']")
    openTabButton = (By.ID, "opentab")

    # iframe
    rahulShettyFrameTitle = "Selenium, API Testing, Software Testing & More QA Tutorials | Rahul Shetty Academy"
    frameLocator = (By.ID, "courses-iframe")
    frameName = "iframe-name"
    loadingIcon = (By.CSS_SELECTOR, ".page-wrapper .preloader span")

    # Hover
    mouseHoverLegend = (By.XPATH, "//legend[text()='Mouse Hover Example']")
    mouseHoverButton = (By.ID, "mousehover")
    mouseHoverDropdown = (By.CSS_SELECTOR, ".mouse-hover .mouse-hover-content")
    mouseHoverDropdownOptions = ["Top", "Reload"]

    # Fixed table
    fixedTable = (By.CSS_SELECTOR, ".tableFixHead #product")
    tableRows = (By.CSS_SELECTOR, ".tableFixHead #product tbody tr td:nth-child(1)")

    """ Handle alerts """

    def verify_practice_page_is_loaded(self):
        """ Method to verify 'Practice Page' is loaded """
        self.wait_for_url_matches(self.pageUrl)
        pageTitle = self.get_page_title()
        assert pageTitle == self.pageTitle
        assert self.is_element_displayed(self.appLogo)

    def enter_text_in_alret_box(self, text: str):
        """ Method to enter value in alert text box """
        self.enter_value_in_text_field(self.alertTextField, text)

    def click_on_alert_button(self):
        """ Method to click on alert button """
        self.click_on_element(self.alretButton)
        time.sleep(1)

    def click_on_confirm_button(self):
        """ Method to click on alert button """
        self.click_on_element(self.confirmButton)
        time.sleep(1)

    def verify_correct_alert_text_is_displayed(self, text):
        """ Method to verify correct alert text is displayed """
        self.verify_alert_text(self.alertText.format(text))

    def verify_correct_alert_confirm_text_is_displayed(self, text):
        """ Method to verify correct alert text is displayed """
        self.verify_alert_text(self.alertConfirmText.format(text))

    def accept_alert(self):
        """ Accept alert """
        return super().accept_alert()
    
    def dismiss_alert(self):
        """ Dismiss alert """
        return super().dismiss_alert()
    
    """ Handle Windows """
    
    def verify_switch_window_handle_legend_is_displayed(self):
        assert self.is_element_displayed(self.switchWindowLegend)

    def click_on_open_window_button(self):
        self.click_on_element(self.openWindowButton)

    """ Handle Tabs """

    def verify_switch_tab_legend_is_displayed(self):
        assert self.is_element_displayed(self.switchTabLegend)

    def click_on_open_tab_button(self):
        self.click_on_element(self.openTabButton)

    """ Handle iFrame """

    def verify_frame_is_displayed(self):
        assert self.is_element_displayed(self.frameLocator)
        self.scroll_to_view_element(self.frameLocator)

    def switch_to_frame(self):
        self.switch_to_frame_by_index(0)
        self.wait_for_element_to_be_invisible(self.loadingIcon)
    
    def switch_to_rahul_shetty_academy_frame_by_locator(self):
        self.switch_to_frame_by_locator(self.frameLocator)
        self.wait_for_element_to_be_invisible(self.loadingIcon)

    def switch_to_rahul_shetty_academy_frame_by_name(self):
        self.switch_to_frame_by_name(self.frameName)
        self.wait_for_element_to_be_invisible(self.loadingIcon)

    def verify_rahul_shetty_academy_course_page_is_correcly_displayed(self):
        pageTitle = self.get_iframe_page_title()
        assert pageTitle == self.rahulShettyFrameTitle, f"Expected: {self.rahulShettyFrameTitle}, Actual: {pageTitle}"

    """ Mouse Hover """
    
    def verify_mouser_hover_legend_is_displayed(self):
        assert self.is_element_displayed(self.mouseHoverLegend)

    def hover_over_mouse_hover_button(self):
        self.scroll_to_view_element(self.mouseHoverButton)
        self.hover_over_element(self.mouseHoverButton)

    def verify_mouse_hover_dropdown_is_displayed(self):
        assert self.is_element_displayed(self.mouseHoverDropdown)

    def verify_mouse_hover_dropdown_options_are_correct(self):
        mouseHoverDropdown = self.wait_and_find_element(self.mouseHoverDropdown)
        dropdownOptions = self.wait_and_find_nested_elements(mouseHoverDropdown, (By.TAG_NAME, "a"))
        for option in dropdownOptions:
            assert option.text in self.mouseHoverDropdownOptions

    """ Fixed table """

    def scroll_fixed_table(self):
        self.scroll_dropdown(self.fixedTable[1], 100)

    def verify_last_table_row_is_displayed(self):
        table = self.wait_and_find_element(self.fixedTable)
        rows = self.wait_and_find_nested_elements(table, self.tableRows)
        assert rows[-1].is_displayed()
