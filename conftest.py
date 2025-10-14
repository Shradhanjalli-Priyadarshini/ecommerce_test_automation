import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")

@pytest.fixture(scope="session")
def base_url():
    """Provide the base URL for the test session."""
    return BASE_URL
    driver.get_screenshot_as_png()

@pytest.fixture(scope="function")
def driver(base_url):
    """Initialize and yield a Chrome WebDriver instance."""
    chrome_options = Options()
    headless = os.getenv("HEADLESS", "false").lower() not in ("0", "false", "no")

    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
    else:
        chrome_options.add_argument("--start-maximized")

    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print(f"\nLaunching browser at: {base_url}")
    driver.get(base_url)
    driver.implicitly_wait(8)

    yield driver

    driver.quit()
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshot automatically on test failure and attach to Allure report.
    """
    outcome = yield
    result = outcome.get_result()

    # Run only when the test has failed during the call phase
    if result.when == "call" and result.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"{item.name}_{timestamp}.png"
                screenshot_path = f"./reports/{screenshot_name}"
                driver.save_screenshot(screenshot_path)

                # Attach to Allure report
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"Failure Screenshot - {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                print(f"📸 Screenshot captured: {screenshot_path}")

            except Exception as e:
                print(f"⚠️ Failed to capture screenshot: {e}")
