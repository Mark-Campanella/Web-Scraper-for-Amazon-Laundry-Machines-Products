import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import pandas as pd

# -----------------------------------------Customization Variables---------------------------------------------------

url = "https://www.amazon.com.br"
keywords = "Lavadora e Secadoraa de Roupas"

# Navigation classes
class_search_bar = 'nav-input.nav-progressive-attribute'
class_submit_btn = 'nav-search-submit-button'
class_next_btn = 's-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator'

# For each item
class_itens = 's-result-item.s-asin'

# URLs (they are analogs)
class_link = 'a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal'

# Item classes DEPRECATED 
att_img = 'data-image-source-density'
class_local_currency = "a-price-symbol"

# For these ones we would need to be inside the products page
class_name = 'a-size-large.product-title-word-break'
class_price = "a-price-whole"
class_marketing_claims_div = "productDescription"
xpath_prod_description = '//*[@id="productDescription"]/p/span/text()'
xpath_img_1 = ''
class_th = "a-color-secondary.a-size-base.prodDetSectionEntry"
class_td = 'a-size-base.prodDetAttrValue'
class_5_Star = 'reviewCountTextLinkedHistogram.noUnderline'

# Global Variables
next_page = None
product_link = []
products_data = []

# Driver Configuration - prioratazing safety and discretion (trying at least)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-geolocation")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-extensions")
languages = ["pt-BR", "pt"]
driver = webdriver.Chrome(options=chrome_options)

# configure Selenium Stealth
stealth(driver,
        languages=languages,
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------#
def scrape_page(driver):
    global product_link
    global next_page

    # wait until elements are found
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_itens)))

    # get elements links
    elements = driver.find_elements(By.CLASS_NAME, class_itens)
    for element in elements:
        item = element.find_element(By.CLASS_NAME, class_link)
        product_link.append(item.get_attribute('href'))

    # Uncomment after testing:
    # try:
    #     next_page = driver.find_element(By.CLASS_NAME, class_next_btn).get_attribute("href")
    # except:
    #     next_page = None

def process_product(driver, link):
    global products_data
    driver.get(link)
    driver.implicitly_wait(20)

    product_info = {'product_link': link}

    try:
        name = driver.find_element(By.CLASS_NAME, class_name).text
        product_info['product_name'] = name
    except:
        product_info['product_name'] = ""

    try:
        price = driver.find_element(By.CLASS_NAME, class_price).text
        product_info['product_price'] = price
    except:
        product_info['product_price'] = ""

    try:
        th_elements = driver.find_elements(By.CLASS_NAME, class_th)
        td_elements = driver.find_elements(By.CLASS_NAME, class_td)
        th_texts = [elem.text for elem in th_elements]
        td_texts = [elem.text for elem in td_elements]

        try:
            five_stars = driver.find_element(By.CLASS_NAME, class_5_Star).get_attribute('title')
        except:
            five_stars = None

        for th_text, td_text in zip(th_texts, td_texts):
            if th_text == "Avaliações de clientes":
                product_info[th_text] = five_stars
            elif th_text == "Ranking dos mais vendidos":
                product_info[th_text] = ""
            else:
                product_info[th_text] = td_text
    except Exception as e:
        print("Error: ", e)
    try:
        description = driver.find_elements(By.CLASS_NAME,xpath_prod_description).text
    except:
        description = None
    finally:
        product_info["Description"] = description
        
    products_data.append(product_info)

def process_products(driver):
    global product_link
    for link in product_link:
        process_product(driver, link)
    product_link.clear()

# Start!
try:
    driver.get(url)
    driver.implicitly_wait(20)
    search = driver.find_element(By.CLASS_NAME, class_search_bar)
    search.send_keys(keywords)
    time.sleep(1)
    search_btn = driver.find_element(By.ID, class_submit_btn)
    search_btn.click()
    driver.implicitly_wait(5)
    while True:
        scrape_page(driver)
        if next_page:
            driver.get(next_page)
        else:
            break

    process_products(driver)

finally:
    driver.quit()

    # Converter a lista de dicionários em um DataFrame
    df = pd.DataFrame(products_data)
    print(df)
    df.to_csv('product_data.csv', index=False)
