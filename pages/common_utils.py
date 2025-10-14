from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def handle_js_alert(driver, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(lambda d: d.switch_to.alert)
        alert = driver.switch_to.alert
        print("Alert found:", alert.text)
        alert.accept()
        return True
    except NoAlertPresentException:
        return False
    except TimeoutException:
        return False

def handle_html_popup(driver):
    try:
        ok_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='OK' or contains(text(),'Ok')]"))
        )
        ok_button.click()
        return True
    except TimeoutException:
        return False
