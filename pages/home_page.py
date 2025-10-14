from selenium.webdriver.common.by import By

class HomePage:
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[class*='btn-default']")

    def __init__(self, driver):
        self.driver = driver

    def open(self, base_url):
        self.driver.get(base_url)

    def search_product(self, product_name):
        self.driver.find_element(*self.SEARCH_INPUT).clear()
        self.driver.find_element(*self.SEARCH_INPUT).send_keys(product_name)
        self.driver.find_element(*self.SEARCH_BUTTON).click()
