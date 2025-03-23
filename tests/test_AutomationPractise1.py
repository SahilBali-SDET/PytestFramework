import pytest
from Resources.PropertyLoader import PropertyLoader
from TestData.HomePageData import HomePageData
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
    greenKartPage = homePage.click_on_automation_practise1_link()
    global GREEN_KART_PAGE_URL
    GREEN_KART_PAGE_URL = greenKartPage.get_current_url()

@pytest.mark.usefixtures("setup_class")
class Test_GreenKartPage(BaseClass):

    def teardown_method(self, method):
        greenKartPage = GreenKartPage(self.driver)

        self.navigate_to_url(GREEN_KART_PAGE_URL)
        greenKartPage.verify_green_kart_page_is_loaded()

    @pytest.mark.greenKartSuite
    def test_VerifyGreenKartPageIsCorrectlyLoaded(self):
        greenKartPage = GreenKartPage(self.driver)

        greenKartPage.verify_green_kart_page_is_loaded()

    @pytest.mark.greenKartSuite
    def test_VerifyUserIsAbleToSearchItems(self):
        greenKartPage = GreenKartPage(self.driver)

        greenKartPage.verify_correct_result_is_displayed_on_searching("Beetroot")

    @pytest.mark.greenKartSuite
    @pytest.mark.xfail(reason="BUG: ENG-001")
    def test_VerifyUserIsAbleToSearchItemsWithSpaceCharacterInPrefix(self):
        greenKartPage = GreenKartPage(self.driver)

        greenKartPage.verify_correct_result_is_displayed_on_searching(" Beetroot")

@pytest.mark.usefixtures("setup_class")
class Test_CheckOutTab(BaseClass):

    @pytest.mark.greenKartSuite
    def test_AddItemsAndCheckout(self):
        greenKartPage = GreenKartPage(self.driver)
        itemName = "Beetroot"
        cartDetails = {"productName": itemName, "productPrice": "32", "productQuantity": "1", "productAmount": "32"}

        greenKartPage.verify_correct_result_is_displayed_on_searching(itemName)
        greenKartPage.search_and_add_item_to_cart(itemName)
        checkOutTab = greenKartPage.click_on_cart_icon()
        checkOutTab.verify_product_details_in_cart(cartDetails)
        checkOutTab.click_on_proceed_to_check_out_button()

    @pytest.mark.greenKartSuite
    def test_ConfirmOrder(self):
        confirmPage = ConfirmPage(self.driver)
        
        confirmPage.verify_confirm_page_is_loaded()
        confirmPage.click_on_place_order_button()
        confirmPage.wait_until_select_country_page_is_laoded()
        confirmPage.select_country_from_dropdown("India")
        confirmPage.check_agree_to_terms_checkbox()
        confirmPage.click_on_proceed_button()
        confirmPage.verify_success_message_is_displayed()

    @pytest.mark.greenKartSuite
    def test_verifySuccessMessageIsDisplayedInGreenColor(self):
        confirmPage = ConfirmPage(self.driver)

        confirmPage.verify_success_message_is_displayed_in_green_color()
