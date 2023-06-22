#######################################################################################################################

# Following code is to get the short description of each product


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from globalFunction import *
import pandas as pd
import re

# get the path of the chrom webdriver, so to automate the process
path = 'C:\Program Files (x86)\chromedriver.exe'
# select the browset you wanna use and define the driver path to it
driver = webdriver.Chrome(path)

# source_url = 'https://www.airease.com/'
source_url = 'https://www.airease.com/products/gas-furnaces/'

driver.get(source_url)

try:
    element = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,"onetrust-reject-all-handler"))
    )
    element.click()
except:
    pass

# (findElement(driver,By.LINK_TEXT,'PRODUCTS')).click()

# medias = findElements(driver,By.CLASS_NAME,'media')

# for idx in range(len(medias)):
#     print(f'index value is {idx}')
#     medias = findElements(driver,By.CLASS_NAME,'media')
#     category_link = findElement(medias[idx],By.TAG_NAME,'a')
#     category_name = findElement(medias[idx],By.CLASS_NAME,'media-heading').text
#     category_img = findElement(medias[idx],By.TAG_NAME,'img').get_attribute('src')
#     category_desc = findElement(medias[idx],By.TAG_NAME,'p').text

#     print(category_name)
#     if category_name == 'Omniguard®' or category_name == 'The Pro Series ™ Systems' or category_name == 'Comfort Sync® A3 Thermostat':
#         pass
#     else:
#         category_link.click()

product_cards_count = findElements(driver,By.CLASS_NAME,'media')
print(len(product_cards_count))
for idx in range(len (product_cards_count)):
    product_cards = findElements(driver,By.CLASS_NAME,'media')
    short_name = findElement(product_cards[idx], By.TAG_NAME,'h3')
    if short_name != None:
        short_name = findElement(product_cards[idx], By.TAG_NAME,'h3').text
        product_link = findElement(findElement(product_cards[idx], By.TAG_NAME,'h3'),By.TAG_NAME,'a').get_attribute('href')
        short_desc = (findElement(product_cards[idx],By.TAG_NAME,'ul')).get_attribute('outerHTML')
        image_link_thumbnail = findElement((findElement(product_cards[idx],By.CLASS_NAME,'media-object')),By.TAG_NAME,'img').get_attribute('src')
        rating = findElement((findElement(product_cards[idx],By.CLASS_NAME,'media-object')),By.CLASS_NAME,'rating').text
        certification_flag_thumbnail = findElement(findElement(product_cards[idx],By.CLASS_NAME,'media-overlay'),By.TAG_NAME,'img')
        if certification_flag_thumbnail != None:
            certification_flag_thumbnail = certification_flag_thumbnail.get_attribute('alt')
        print(certification_flag_thumbnail)
        print('='*50)
driver.back()
