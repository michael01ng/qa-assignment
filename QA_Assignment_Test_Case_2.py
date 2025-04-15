from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup WebDriver (Make sure chromedriver is in PATH)
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # 1. Navigate to website
    driver.get("https://rapsodo.com")
    assert "rapsodo.com" in driver.current_url

    # 2. Click on Cart icon and verify cart is empty
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.header-cart-link"))
    ).click()
    
    empty_cart_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Your cart is currently empty')]"))
    )
    assert empty_cart_text.is_displayed()

    # 3. Navigate to Golf > Mobile Launch Monitor
    driver.get("https://rapsodo.com/pages/mlm")
    WebDriverWait(driver, 10).until(
        EC.title_contains("Mobile Launch Monitor")
    )

    # 4. Click "Shop MLM"
    shop_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "SHOP MLM"))
    )
    shop_button.click()

    # 5. Click ADD TO CART
    add_to_cart_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "add"))
    )
    price_element = driver.find_element(By.CLASS_NAME, "price")
    product_price = price_element.text
    add_to_cart_btn.click()

    # 6. Redirect to cart and verify product added
    WebDriverWait(driver, 10).until(
        EC.url_contains("/cart")
    )
    cart_price = driver.find_element(By.CLASS_NAME, "cart__subtotal").text
    assert product_price in cart_price

    # 7. Change quantity to 2
    qty_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "updates[]"))
    )
    qty_input.clear()
    qty_input.send_keys("2")

    # Click update cart if available
    update_btn = driver.find_element(By.NAME, "update")
    update_btn.click()
    time.sleep(3)

    # Verify quantity updated
    updated_qty = driver.find_element(By.NAME, "updates[]").get_attribute("value")
    assert updated_qty == "2"

    print("Test case completed successfully.")

except Exception as e:
    print("Test failed:", e)

finally:
    driver.quit()
