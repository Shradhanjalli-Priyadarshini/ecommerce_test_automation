from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductsPage:
    def __init__(self, driver):
        self.driver = driver

    def add_product_to_cart(self, product_name):
        product_xpath = f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, product_xpath))
        ).click()
        print(f"✅ Added {product_name} to cart")

    def open_cart(self):
        cart_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        )
        cart_icon.click()
        print("🛒 Opened cart page")
