import os
import sys

import pytest
from selenium import webdriver
from pytest_html import extras  # Import pytest_html extras
import logging


#driver = None

# Add the project root to sys.path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#method found on pytest docs to pass command line options at run time in terminal. Adapted to call multiple browsers when testing
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome",
        choices=["chrome", "firefox", "edge"],  # Restrict to valid options
        help="Choose browser: chrome, firefox, or edge"
    )
    parser.addoption(
        "--url", action="store", default="https://rahulshettyacademy.com/angularpractice",
        help="Specify the base URL for testing"
    )

#scope class makes it be executed only once when class is called
@pytest.fixture(scope="class", params=[
    (375, 812),   # iPhone X
    #(414, 896),   # iPhone XR
   # (768, 1024),  # iPad
   # (1024, 768),  # Small Laptop
    (1366, 768),  # Standard Laptop
])
def setup(request):
    #global driver #this global means the should use the drive declared on the top with none, instead of creating a new variable driver just for this method, this way this driver will be also used in the method bellow to generate screenshot
    browser_name = request.config.getoption("browser_name")
    url = request.config.getoption("url")
    width, height = request.param
    #if driver is None:  # Only create a new browser if one does not exist
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run Chrome in headless mode (doesn't open browser)
        options.add_argument("--disable-gpu")  # Recommended for headless mode on Windows
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(options=options)
    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(options=options)

        driver.implicitly_wait(4)
    driver.set_window_size(width, height)  # Resize browser to given width/height
    driver.get(url)
    request.cls.driver = driver #We're sending the local driver from this fixture to our class (cls) driver
    yield driver
    driver.quit()



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    #Attach logs and screenshots to the HTML report
    pytest_html = item.config.pluginmanager.getplugin('html')
    if pytest_html is None:
        return  # Exit the function if pytest-html is not available

    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    # ✅ Attach logs to report
    log_file = "logfile2.log"  # Adjust this to your actual log file name
    try:
        with open(log_file, "r") as f:
            log_content = f.read()
        if log_content:
            extra.append(extras.text(log_content, "Test Logs"))
    except Exception as e:
        logging.error(f"Error attaching logs: {e}")

    # ✅ Capture and attach screenshot on failure
    if report.when in ["call", "setup"]:
        xfail = hasattr(report, "wasxfail")
        if (report.failed and not xfail) or (report.skipped and xfail):
            if hasattr(item.cls, "driver"):
                file_name = report.nodeid.replace("::", "_") + ".png"
                _capture_screenshot(item.cls.driver, file_name)
                if file_name:
                    html = f'<div><img src="{file_name}" alt="screenshot" style="width:304px;height:228px;" ' \
                           'onclick="window.open(this.src)" align="right"/></div>'
                    extra.append(extras.html(html))

    report.extra = extra


def _capture_screenshot(driver, name):
    #Take a screenshot if WebDriver is available
    try:
        driver.get_screenshot_as_file(name)
    except Exception as e:
        logging.error(f"Failed to capture screenshot: {e}")