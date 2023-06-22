#######################################################################################################################

# Following code is to get the details from detail product page

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
source_url = 'https://www.airease.com/products/gas-furnaces/a951e'

driver.get(source_url)

try:
    element = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,"onetrust-reject-all-handler"))
    )
    element.click()
except:
    pass

product_header_copy = findElement(driver,By.CLASS_NAME,'product-header-copy')
long_name = findElement(product_header_copy,By.TAG_NAME,'h1').text
sub_desc = findElement(product_header_copy,By.TAG_NAME,'p').text
product_certifications = findElement(product_header_copy,By.CLASS_NAME,'product-certifications')
product_certifications_flag = findElements(product_certifications,By.TAG_NAME,'img')
product_certifications_flag = [item.get_attribute('src') for item in product_certifications_flag]

product_header_img = findElement(driver,By.CLASS_NAME,'product-header-img')
image_link = findElement(product_header_img,By.TAG_NAME,'img').get_attribute('src')

tabs = findElements(driver,By.CLASS_NAME,'tab-pane')
nav_tabs = findElements(findElement(driver,By.CLASS_NAME,'nav-tabs'),By.TAG_NAME,'a')
tab_combine = zip(nav_tabs,tabs)
for nav,tab in tab_combine:
    nav.click()
    h3 = findElement(tab,By.TAG_NAME,'h3').get_attribute('text')
    long_desc = findElements(findElement(tab,By.TAG_NAME,'ul'),By.TAG_NAME,'li')
    print(len(long_desc))

    # there is a difference in structure for top features tab and other tab