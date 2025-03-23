import os
import pytest
import pytest_html
from pytest_html import extras
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from Resources.PropertyLoader import PropertyLoader

driver = None
URL = PropertyLoader.get_url()

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="firefox"
    )

@pytest.fixture(scope="class")
def setup(request):
    global driver
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--guest")
        # service_obj = Service("./webdrivers/windows/chromedriver.exe")
        service_obj = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service_obj, options=chrome_options)
    elif browser_name == "firefox":
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--disable-extensions')
        firefox_options.add_argument('--disable-dev-shm-usage')
        firefox_options.add_argument('--disable-gpu')
        service_obj = Service("./webdrivers/windows/geckodriver.exe")
        # service_obj = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service_obj, options=firefox_options)
    else:
        print("Invalid browser option")

    print("Browser started")
    driver.get(URL)
    driver.maximize_window()
    request.cls.driver = driver

    yield
    print("Browser closed")
    driver.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    if report.failed and report.when == "call":
        # always add url to report
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            extras.append(pytest_html.extras.html("<div>Additional HTML</div>"))
        report.extras = extras
