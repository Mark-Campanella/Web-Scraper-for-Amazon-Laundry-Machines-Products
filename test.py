import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd

my_location = "Brazil"
zip_code = 19947

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-geolocation")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--lang=en")
languages = ["en", "en"] #In case of going for the USA/UK or anywhere, CHANGE THIS

driver = webdriver.Chrome(options=chrome_options)
stealth(driver,
        languages=languages,
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

driver.get("https://www.amazon.com")
driver.implicitly_wait(20)
location = str(driver.find_element(By.ID,"glow-ingress-line2").text).strip().replace(" ", "")
if location == my_location:
    # Wait for the location icon to be present and click it
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "nav-packard-glow-loc-icon"))
    )
    driver.find_element(By.ID, "nav-packard-glow-loc-icon").click()

    # Wait for the ZIP input field to be present and send ZIP code
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput"))
    )
    zip_input = driver.find_element(By.ID, "GLUXZipUpdateInput")
    zip_input.send_keys(zip_code, Keys.ENTER)  # Replace with your actual ZIP code

    # Send Enter key using send_keys method
    zip_input.send_keys(Keys.ENTER)

    # Optional: Use JavaScript to trigger Enter key event
    driver.execute_script(
        "arguments[0].dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter'}));", zip_input
    )

    # Optional: Use ActionChains to send Enter key
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER).perform()

    # Adding a sleep to ensure actions are completed (optional, use WebDriverWait for better handling)
    time.sleep(5)
                       
else: print("Ops, something went wrong")
time.sleep(5)
driver.quit()




        