from selenium import webdriver
from selenium.webdriver.common.by import By
import time

link = "https://www.amazon.com.br/s?k=m%C3%A1quinas+%2B+de+%2B+lavar+%2B+e+%2B+secadoras&i=appliances&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1715947464&rnid=16254006011&ref=sr_nr_p_36_0_0&low-price=290&high-price="
class_urls = "a-link-normal.s-no-outline"
class_model_description = "a-size-large.product-title-word-break"
class_price = "a-price-whole"
class_local_currency = "a-price-symbol"
class_marketing_claims = "productDescription"
class_5_Star = "a-icon-alt"
machines=[{}]

def get_links():
    urls = []
    driver = webdriver.Chrome()

    try:
        driver.get(link)
    except ConnectionRefusedError as e:
        print("I was unable to open the link: ", e)
        
    try:
        driver.implicitly_wait(5)
        elem = driver.find_elements(By.CLASS_NAME,class_urls)
        for url in elem: 
            if url: urls.append(url.get_attribute("href"))
    except RuntimeError as e:
        print("I was unable to get the element: ", e)
    finally:
        driver.quit()
    return urls

def get_info(urls):
    
    for url in urls:
        machine = {}
        machine['url'] = url
        driver = webdriver.Chrome()
        try:
            driver.get(url)
            time.sleep((2))
        except ConnectionRefusedError as e:
            print("I was unable to open the link: ", e)    
        
        try:
            driver.implicitly_wait(5)
            machine['model_description'] = (driver.find_element(By.CLASS_NAME, class_model_description)).text()
            time.sleep(5)
            machine['local_currency'] = (driver.find_element(By.CLASS_NAME, class_local_currency)).text()
            time.sleep((4,5))
            machine['price'] = (driver.find_element(By.CLASS_NAME, class_price)).text()
            time.sleep((4))
            machine['marketing_claims'] = (driver.find_element(By.CLASS_NAME, class_marketing_claims)).find_element((By.TAG_NAME,'span')).text()
            time.sleep((3))
            machine['price'] = driver.find_element((By.CLASS_NAME, class_price)).text()
            time.sleep((1))
            machine['5_Star'] = driver.find_element((By.CLASS_NAME, class_5_Star)).text()
        except Exception as e:
            print("Object not found, error message: ", e)
        finally:
            time.sleep((3))
            driver.quit()
            machines.append(machine)

urls = get_links()
get_info(urls)
print(machines)

