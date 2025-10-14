import pytest
import allure
from selenium.common import NoAlertPresentException
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.title("E2E Checkout Flow")
@allure.description("Launch site, login, add product to cart, checkout and verify confirmation message.")
@pytest.mark.e2e
def test_end_to_end_checkout(driver):
    login_page = LoginPage(driver)
    products_page = ProductsPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    with allure.step("Step 1: Login"):
        login_page.login("standard_user", "secret_sauce")

        try:
            alert = driver.switch_to.alert
            alert.accept()
            print("✅ JS alert accepted.")
        except NoAlertPresentException:
            print("No JS alert appeared after login.")

    with allure.step("Step 2: Add product and open cart"):
        products_page.add_product_to_cart("Sauce Labs Backpack")
        products_page.open_cart()

    with allure.step("Step 3: Proceed to checkout"):
        cart_page.proceed_to_checkout()

    with allure.step("Step 4: Fill details and finish order"):
        checkout_page.fill_details_and_continue("John", "Doe", "12345")
        checkout_page.finish_order()

    with allure.step("Step 5: Validate order confirmation"):
        msg = checkout_page.get_confirmation_message()
        assert msg == "Thank you for your order!", f"❌ Unexpected confirmation: {msg}"
        print("✅ Order placed successfully!")
