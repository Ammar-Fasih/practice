#######################################################################################################################

# Following code is to get all the elements from airease.com in order to do further analysis

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from globalFunction import *
import pandas as pd
import re


# get the path of the chrom webdriver, so to automate the process
path = 'C:\Program Files (x86)\chromedriver.exe'
# select the browset you wanna use and define the driver path to it
driver = webdriver.Chrome(path)

category_df = pd.DataFrame(columns=['category','cat_image','cat_desc','cat_link'])
product_df = pd.DataFrame(columns=['short_name','short_desc','image_link_thumbnail','rating','certification_flag_thumbnail','long_name','sub_desc','product_certifications_flag','image_link','h3','long_desc'])

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

df = pd.DataFrame(columns=['heading','desc'])

for idx in range(len(medias)):
    cat_list = []
    medias = findElements(driver,By.CLASS_NAME,'media')
    category_link = findElement(medias[idx],By.TAG_NAME,'a')
    category_name = findElement(medias[idx],By.CLASS_NAME,'media-heading').text

    if category_name == 'Omniguard®' or category_name == 'The Pro Series ™ Systems' or category_name == 'Comfort Sync® A3 Thermostat':
        pass
    else:
        category_link.click()

        product_cards_count = findElements(driver,By.CLASS_NAME,'media')
        product_list = []
        for idx in range(len (product_cards_count)):
            product_cards = findElements(driver,By.CLASS_NAME,'media')
            short_name = findElement(product_cards[idx], By.TAG_NAME,'h3')
            if short_name != None:
                product_link = findElement(findElement(product_cards[idx], By.TAG_NAME,'h3'),By.TAG_NAME,'a').get_attribute('href')
              
                driver.get(product_link)

                product_header_copy = findElement(driver,By.CLASS_NAME,'product-header-copy')
                long_name = findElement(product_header_copy,By.TAG_NAME,'h1').text
                sub_desc = findElement(product_header_copy,By.TAG_NAME,'p').text

                tabs = findElements(driver,By.CLASS_NAME,'tab-pane')
                nav_tabs = findElements(findElement(driver,By.CLASS_NAME,'nav-tabs'),By.TAG_NAME,'a')
                tab_combine = zip(nav_tabs,tabs)
                for nav,tab in tab_combine:
                    nav.click()
                    if nav.text == 'TOP FEATURES':
                        objs = findElements(findElement(tab,By.TAG_NAME,'ul'),By.TAG_NAME,'li')
                        for obj in objs:
                            h = findElement(obj,By.TAG_NAME,'h4').text
                            p = findElement(obj,By.TAG_NAME,'p').text
                            print(p,h)
                            df_list = [h,p]
                            df = pd.concat([df,pd.DataFrame([df_list],columns=df.columns)],ignore_index=True)
                    else:
                        objs = findElement(tab,By.TAG_NAME,'ul')
                        h = findElements(objs,By.TAG_NAME,'h4')
                        p = findElements(objs,By.TAG_NAME,'p')
                        objs = zip(h,p)
                        for h,p in objs:
                            print(p.text,h.text)
                            df_list = [h.text,p.text]
                            df = pd.concat([df,pd.DataFrame([df_list],columns=df.columns)],ignore_index=True)
            
                    df.to_csv('longdesc3_compare.csv',index=False)
                driver.back()
        driver.back()
