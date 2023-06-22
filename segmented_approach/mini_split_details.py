#######################################################################################################################

# Following code is to get the details from mini split page, since it's structure is entirely different from rest of the product pages

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from globalFunction import *
import pandas as pd
import re

product_df = pd.DataFrame(columns=['short_name','short_desc','image_link_thumbnail','slug','category','meta_title','meta_keywords','meta_description','rating','certification_flag_thumbnail','long_name','intro','product_certifications_flag','image_link','long_desc'])


# get the path of the chrom webdriver, so to automate the process
path = 'C:\Program Files (x86)\chromedriver.exe'
# select the browset you wanna use and define the driver path to it
driver = webdriver.Chrome(path)

# source_url = 'https://www.airease.com/'
source_url = 'https://www.airease.com/products/mini-split-systems'

driver.get(source_url)

try:
    element = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,"onetrust-reject-all-handler"))
    )
    element.click()
except:
    pass

product_cards = findElements(findElement(driver,By.ID,'ProductThumbnails'),By.CLASS_NAME,'row')
for product in product_cards:
    long_name = findElement(product,By.TAG_NAME,'h3').text
    intro = findElement(product,By.TAG_NAME,'h4').text + '\n' + findElement(product,By.TAG_NAME,'p').text
    certification_flag_thumbnail = findElement(product,By.CLASS_NAME,'energy-star')
    long_desc = findElement(product,By.TAG_NAME,'ul').get_attribute('outerHTML')
    image_link = findElement(product,By.TAG_NAME,'img').get_attribute('src')
    print(image_link)