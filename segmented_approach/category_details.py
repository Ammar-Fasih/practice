#######################################################################################################################

# Following code is to get ONLY the category details (image, title, para) to be saved in csv

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

source_url = 'https://www.airease.com/'

driver.get(source_url)

try:
    element = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,"onetrust-reject-all-handler"))
    )
    element.click()
except:
    pass

(findElement(driver,By.LINK_TEXT,'PRODUCTS')).click()

medias = findElements(driver,By.CLASS_NAME,'media')

for idx in range(len(medias)):
    print(f'index value is {idx}')
    # medias = findElements(driver,By.CLASS_NAME,'media')
    category_link = findElement(medias[idx],By.TAG_NAME,'a')
    category_name = findElement(medias[idx],By.CLASS_NAME,'media-heading').text
    category_img = findElement(medias[idx],By.TAG_NAME,'img').get_attribute('src')
    category_desc = findElement(medias[idx],By.TAG_NAME,'p').text
    print(category_name)
    print(category_link)
    print(category_img)
    print(category_desc)
    print('x'*50)