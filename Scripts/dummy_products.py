from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
import json

def download_image(image_url : str, image_filename : str):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content
        with open(image_filename, "wb") as f:
            f.write(image_data)
        print(f"Image downloaded and saved as {image_filename}")
    else:
        print("Failed to download the image")


def search_amazon_site(driver : webdriver.Firefox, search_word : str):
    driver.get("https://www.amazon.com/")
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys(search_word)
    search_button = driver.find_element(By.ID, "nav-search-submit-button")
    search_button.click()
    

def get_plp_data(driver : webdriver.Firefox):
    product_list = []
    product_links = driver.find_elements(By.CSS_SELECTOR,'.a-link-normal.s-no-outline')
    driver_pdp = launch_webdriver()
    for product_link in product_links[0:25]:
        link = product_link.get_attribute("href")
        product = get_pdp_data(link=link, driver_pdp=driver_pdp)
        product_list.append(product)
    return product_list
        
    
def get_pdp_data(link : str, driver_pdp : webdriver.Firefox):
    driver_pdp.get(link)
    product_id = link.split("/")[-2]
    feature_list = driver_pdp.find_elements(By.CSS_SELECTOR, "#feature-bullets .a-list-item")
    features = ""
    for feature in feature_list[:-1]:
        features += feature.text + "\n"
    features += feature_list[-1].text
    images = driver_pdp.find_elements(By.CSS_SELECTOR, ".a-button-thumbnail > .a-button-inner > .a-button-text > img")
    os.mkdir(product_id)
    for img in images[1:]:
        image_url = img.get_attribute('src')
        download_image(image_url=image_url.replace("40","695"), image_filename= product_id + "/" + image_url.replace("40","695").split("/")[-1])
    return {
        "product_id" : product_id,
        "product_description" : features,
        "brand" : "Addidas"
    }
    
def launch_webdriver() -> webdriver.Firefox:
    driver = webdriver.Firefox(executable_path='./Firefox/geckodriver.exe')
    return driver

driver = launch_webdriver()
search_amazon_site(driver=driver,search_word="Adidas Shoes")
products = get_plp_data(driver=driver)
with open('adidas.json', 'w') as file:
    data = json.dumps(products)
    file.write(data)
