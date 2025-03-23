import inspect
import logging
import time
import pytest
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert 
from selenium.webdriver.common.action_chains import ActionChains

loggerName = inspect.stack()[1][3]
log = logging.getLogger(loggerName)
fileHandler = logging.FileHandler('logfile.log')
formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
fileHandler.setFormatter(formatter)
log.addHandler(fileHandler)  # file handler object
log.setLevel(logging.DEBUG)

@pytest.mark.usefixtures("setup")
class BaseClass:

    def refresh_page(self):
        self.driver.refresh()

    def highlight_element(self, web_element: WebElement):
        self.driver.execute_script("arguments[0].setAttribute('style', 'background: yellow; border: 2px solid blue;');", web_element)

    def unhighlight_element(self, web_element: WebElement):
        time.sleep(.04)
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", web_element, "")

    def presence_of_element_located(self, locator: tuple, timeout: int = 15)-> WebElement:
        """ Method to verify presence of element is located """
        driver = WebDriverWait(self.driver, timeout)
        try:
            web_element = driver.until(EC.presence_of_element_located((locator[0], locator[1])))
            self.highlight_element(web_element)
            log.info(f"fLocator property: {locator[0]} with value: {locator[1]} is present on page")
            self.unhighlight_element(web_element)
            return web_element
        except TimeoutException:
            raise NoSuchElementException(f"Locator property: {locator[0]} with value: {locator[1]} is not present on page")

    def wait_and_find_element(self, locator: tuple) -> WebElement:
        web_element = self.presence_of_element_located(locator, 10)
        if web_element.is_displayed():
            log.info(f"Locator property: {locator[0]} with value: {locator[1]} is visible on page")
            return web_element
        else:
            raise NoSuchElementException(f"Locator property: {locator[0]} with value: {locator[1]} isn't visible on page")

    def wait_and_find_elements(self, locator: tuple) -> list[WebElement]:
        driver = WebDriverWait(self.driver, 10)
        try:
            driver.until(EC.presence_of_element_located(locator))
            web_elements = self.driver.find_elements(*locator)
            return web_elements
        except TimeoutException:
            web_elements = []
            logging.error(f"No locator with property: {locator[0]} & value: {locator[1]} is visible on page")
            return web_elements

    def find_element(self, locator: tuple) -> WebElement:
        web_element = self.driver.find_element(locator[0], locator[1])
        return web_element

    def click_on_element(self, locator: tuple) -> None:
        web_element = self.wait_and_find_element(locator)
        web_element.click()
        log.info("Able to click on link/button having locator property: {} and property value: {}".format(locator[0], locator[1]))

    def enter_value_in_text_field(self, locator: tuple, text: str):
        web_element = self.wait_and_find_element(locator)
        web_element.send_keys(Keys.CONTROL, "a")
        web_element.send_keys(Keys.DELETE)
        web_element.send_keys(text)

    def enter_value_in_text_field_in_captial_letter(self, locator: tuple, text: str):
        web_element = self.wait_and_find_element(locator)
        web_element.send_keys(Keys.CONTROL, "a")
        web_element.send_keys(Keys.DELETE)
        web_element.send_keys(Keys.SHIFT, text)

    def get_element_text(self, locator: tuple):
        web_element = self.wait_and_find_element(locator)
        return web_element.text

    def verify_link_presence(self, text: str):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, text)))

    def select_option_by_text(self, locator, text: str) -> None:
        dropdown = self.wait_and_find_element(locator)
        sel = Select(dropdown)
        sel.select_by_visible_text(text)

    def is_element_displayed(self, locator: tuple, timeout: int = 15)-> bool:
        """ Method to verify element is displayed on page """
        driver = WebDriverWait(self.driver, timeout)
        try:
            driver.until(EC.visibility_of_element_located((locator[0], locator[1])))
            log.info(f"Locator property: {locator[0]} with value: {locator[1]} is displayed on page")
            return True
        except TimeoutException:
            log.error(f"Locator property: {locator[0]} with value: {locator[1]} is not displayed on page")
            return False
 
    def is_element_present(self, locator: tuple, timeout: int = 15)-> bool:
        """ Method to verify element is present on DOM """
        driver = WebDriverWait(self.driver, timeout)
        try:
            driver.until(EC.presence_of_element_located((locator[0], locator[1])))
            log.info(f"Locator property: {locator[0]} with value: {locator[1]} is present in DOM")
            return True
        except TimeoutException:
            log.error(f"Locator property: {locator[0]} with value: {locator[1]} is not preesnt in DOM")
            return False
        
    def is_text_displayed(self, expected_text: str, timeout: int = 15)-> bool:
        """ Method to verify a text is not displayed on page """
        driver = WebDriverWait(self.driver, timeout)
        try:
            driver.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text()='{}')]".format(expected_text))))
            log.info(f"Text {expected_text} is displayed on page")
            return True
        except TimeoutException:
            log.info(f"Text {expected_text} is not displayed on page")
            return False

    def element_should_not_be_displayed(self, locator: tuple, timeout: int = 2)-> bool:
        """ Method to verify element is not displayed on page """
        driver = WebDriverWait(self.driver, timeout)
        try:
            driver.until(EC.invisibility_of_element_located((locator[0], locator[1])))
            log.info(f"Locator property: {locator[0]} with value: {locator[1]} is not displayed on page")
            return True
        except TimeoutException:
            log.error(f"Locator property: {locator[0]} with value: {locator[1]} is displayed on page")
            return False

    def get_page_title(self):
        pageTitle = self.driver.title
        return pageTitle
 
    def get_current_url(self):
        return self.driver.current_url

    def navigate_to_url(self, url):
        return self.driver.get(url)
 
    def wait_for_url_to_change(self, oldUrl, timeout: int = 15)-> WebElement:
        """ Method to wait until url changes """
        driver = WebDriverWait(self.driver, timeout)
        try:
            driver.until(EC.url_changes(oldUrl))
        except TimeoutException:
            raise Exception(f"Url didn't changed in {timeout} seconds")
        
    def wait_for_url_matches(self, url, timeout: int = 15)-> WebElement:
        """ Method to wait until matches """
        driver = WebDriverWait(self.driver, timeout)
        try:
            driver.until(EC.url_to_be(url))
        except TimeoutException:
            raise Exception(f"Url didn't changed in {timeout} seconds")
        
    def wait_for_element_to_be_visible(self, locator: tuple, timeout: int = 15)-> WebElement:
        """ Method to element to be visible on page """
        driver = WebDriverWait(self.driver, timeout)
        try:
            web_element = driver.until(EC.visibility_of_element_located((locator[0], locator[1])))
            log.info(f"Locator property: {locator[0]} with value: {locator[1]} is invisible on page")
            return web_element
        except TimeoutException:
            raise NoSuchElementException(f"Locator property: {locator[0]} with value: {locator[1]} is still displayed on page")
        
    def wait_for_element_to_be_invisible(self, locator: tuple, timeout: int = 15)-> WebElement:
        """ Method to element to be invisible on page """
        driver = WebDriverWait(self.driver, timeout)
        try:
            web_element = driver.until(EC.invisibility_of_element_located((locator[0], locator[1])))
            log.info(f"Locator property: {locator[0]} with value: {locator[1]} is invisible on page")
            return web_element
        except TimeoutException:
            raise NoSuchElementException(f"Locator property: {locator[0]} with value: {locator[1]} is still displayed on page")

    def wait_and_find_nested_element(self, parentElement: WebElement, childElementlocator: tuple, timeout: int = 15):
        driver = WebDriverWait(parentElement, timeout)
        try:
            web_element = driver.until(EC.presence_of_element_located(childElementlocator))
            log.info(f"fLocator property: {childElementlocator[0]} with value: {childElementlocator[1]} is present on page")
            return web_element
        except TimeoutException:
            raise TimeoutException(f"Locator property: {childElementlocator[0]} with value: {childElementlocator[1]} is not present on page")
        
    def wait_and_find_nested_elements(self, parentElement: WebElement, childElementlocator: tuple, timeout: int = 15):
        driver = WebDriverWait(parentElement, timeout)
        try:
            driver.until(EC.presence_of_element_located(childElementlocator))
            log.info(f"fLocator property: {childElementlocator[0]} with value: {childElementlocator[1]} is present on page")
            web_elements = parentElement.find_elements(*childElementlocator)
            return web_elements
        except TimeoutException:
            web_elements = []
            log.error(f"No elements with locator {childElementlocator} found within parent element")
            return web_elements
        
    def get_css_property(self, locator, propertyName):
        web_element = self.wait_and_find_element(locator)
        return web_element.value_of_css_property(propertyName)
    
    """ Handle Alerts """

    def get_alert_text(self):
        alert = Alert(self.driver) 
        return alert.text

    def verify_alert_text(self, text):
        alertText = self.get_alert_text()
        assert alertText == text, f"Expected: {text}, Actual: {alertText}"

    def accept_alert(self):
        alert = Alert(self.driver) 
        alert.accept()
    
    def dismiss_alert(self):
        alert = Alert(self.driver) 
        alert.dismiss()

    """ Tabs and windows in Selenium are handled the same way because both are treated as separate window handles by the browser. """
    """ Handle windows """
    def switch_to_new_window(self):
        original_window = self.driver.current_window_handle
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

    def switch_to_window_by_title(self, expected_title):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if expected_title in self.driver.title:
                return True  # Successfully switched
        return False  # Title not found

    def switch_to_main_window(self):
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[0])

    def close_current_window(self):
        self.driver.close()
        self.switch_to_main_window()

    """ Handle Tabs """
    def switch_to_new_tab(self):
        original_tab = self.driver.current_window_handle
        for window_handle in self.driver.window_handles:
            if window_handle != original_tab:
                self.driver.switch_to.window(window_handle)
                break

    def switch_to_tab_by_title(self, expected_title):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if expected_title in self.driver.title:
                return True  # Successfully switched
        return False  # Title not found

    def switch_to_main_tab(self):
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[0])

    def close_current_tab(self):
        self.driver.close()
        self.switch_to_main_tab()

    """ Action Chains """

    def hover_over_element(self, locator: tuple):
        action = ActionChains(self.driver)
        web_element = self.wait_and_find_element(locator)
        action.move_to_element(web_element).perform()

    def right_click_on_element(self, locator: tuple):
        action = ActionChains(self.driver)
        web_element = self.wait_and_find_element(locator)
        action.context_click(web_element).perform()

    def hover_and_click_on_element(self, locator: tuple):
        action = ActionChains(self.driver)
        web_element = self.wait_and_find_element(locator)
        action.move_to_element(web_element).click().perform()

    def double_click_on_element(self, locator: tuple):
        action = ActionChains(self.driver)
        web_element = self.wait_and_find_element(locator)
        action.double_click(web_element).perform()

    def drag_and_drop_element(self, draglocator: tuple, dropLocator: tuple):
        action = ActionChains(self.driver)
        drag_element = self.wait_and_find_element(draglocator)
        drop_element = self.wait_and_find_element(dropLocator)
        action.drag_and_drop(drag_element, drop_element).perform()

    def drag_and_release_element(self, draglocator: tuple, dropLocator: tuple):
        action = ActionChains(self.driver)
        drag_element = self.wait_and_find_element(draglocator)
        drop_element = self.wait_and_find_element(dropLocator)
        action.click_and_hold(drag_element)
        action.move_by_offset(100, 0) # activate element
        action.release(drop_element)
        action.perform()

    """ Handle Frames """

    def switch_to_frame_by_index(self, frameIndex: int):
        """ Switch to the frame by index """
        self.driver.switch_to.frame(frameIndex) 

    def switch_to_frame_by_name(self, frameName: str):
        """ Switch to a frame by its name """
        self.driver.switch_to.frame(frameName)

    def switch_to_frame_by_id(self, frameId: str):
        """ Switch to a frame by its id """
        self.driver.switch_to.frame(frameId)

    def switch_to_frame_by_locator(self, frameLocator: tuple):
        """ Switch to a frame by locator """
        frame = self.wait_and_find_element(frameLocator)
        self.driver.switch_to.frame(frame)

    def switch_to_default_content(self):
        """ Switch back to the main content of the page """
        self.driver.switch_to.default_content()

    """ Java Script Executor """

    def get_iframe_page_title(self):
        """ Get the page title of the iframe content """
        return self.driver.execute_script("return document.title;")

    def scroll_to_view_element(self, locator: tuple):
        web_element = self.wait_and_find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", web_element)

    """ Dropdown Scrolling """

    def scroll_dropdown(self, dropdownCSS, scrollBy):
        self.driver.execute_script("""
                                   var dropdownElement = document.querySelector(arguments[0]);
                                   if (dropdownElement) {
                                        dropdownElement.scrollBy(0, arguments[1]);
                                   }
                                   """, 
                                   dropdownCSS, scrollBy)
