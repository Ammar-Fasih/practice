#######################################################################################

# Following code is a conosildated approach to get all details of each product (text and image)

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

category_df = pd.DataFrame(columns=['category','cat_image','cat_desc','cat_link'])
product_df = pd.DataFrame(columns=['short_name','short_desc','image_link_thumbnail','slug','category','meta_title','meta_keywords','meta_description','rating','certification_flag_thumbnail','long_name','intro','product_certifications_flag','image_link','long_desc'])

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
    cat_list = []
    medias = findElements(driver,By.CLASS_NAME,'media')
    category_link = findElement(medias[idx],By.TAG_NAME,'a')
    category_name = findElement(medias[idx],By.CLASS_NAME,'media-heading').text
    category_img = findElement(medias[idx],By.TAG_NAME,'img').get_attribute('src')
    category_desc = findElement(medias[idx],By.TAG_NAME,'p').text
    print(category_name)
    cat_list = [category_name,category_img,category_desc,category_link.get_attribute('href')]
    # category_df = category_df.append(pd.Series(cat_list,index=category_df.columns),ignore_index=True)
    print(category_link.get_attribute('href'))
    if category_name == 'Omniguard®' or category_name == 'The Pro Series ™ Systems' or category_name == 'Comfort Sync® A3 Thermostat':
        pass
    elif category_name == 'Mini-Split Systems':
        category_link.click()
        product_cards = findElements(findElement(driver,By.ID,'ProductThumbnails'),By.CLASS_NAME,'row')
        for product in product_cards:
            long_name = findElement(product,By.TAG_NAME,'h3').text
            intro = findElement(product,By.TAG_NAME,'h4').text + '\n' + findElement(product,By.TAG_NAME,'p').text
            certification_flag_thumbnail = findElement(product,By.CLASS_NAME,'energy-star')
            if certification_flag_thumbnail != None:
                    certification_flag_thumbnail = certification_flag_thumbnail.get_attribute('alt')
            long_desc = findElement(product,By.TAG_NAME,'ul').get_attribute('outerHTML')
            image_link = findElement(product,By.TAG_NAME,'img').get_attribute('src')
        
            product_list = {'long_name':long_name,'intro':intro,'certification_flag_thumbnail':certification_flag_thumbnail,'long_desc':long_desc,'image_link':image_link}
            print(product_list)
            product_df = pd.concat([product_df,pd.DataFrame([product_list],columns=product_df.columns)],ignore_index=True)

            product_df.to_csv('../data/final/product_details_v1.csv',index=False)
        driver.back()
    else:
        category_link.click()

        product_cards_count = findElements(driver,By.CLASS_NAME,'media')
        product_list = []
        for idx in range(len (product_cards_count)):
            product_cards = findElements(driver,By.CLASS_NAME,'media')
            short_name = findElement(product_cards[idx], By.TAG_NAME,'h3')
            if short_name != None:
                short_name = findElement(product_cards[idx], By.TAG_NAME,'h3').text
                product_link = findElement(findElement(product_cards[idx], By.TAG_NAME,'h3'),By.TAG_NAME,'a').get_attribute('href')
                slug = product_link.rsplit('/')[-1]
                short_desc = (findElement(product_cards[idx],By.TAG_NAME,'ul')).get_attribute('outerHTML')
                image_link_thumbnail = findElement((findElement(product_cards[idx],By.CLASS_NAME,'media-object')),By.TAG_NAME,'img').get_attribute('src')
                rating = findElement((findElement(product_cards[idx],By.CLASS_NAME,'media-object')),By.CLASS_NAME,'rating').text
                certification_flag_thumbnail = findElement(findElement(product_cards[idx],By.CLASS_NAME,'media-overlay'),By.TAG_NAME,'img')
                if certification_flag_thumbnail != None:
                    certification_flag_thumbnail = certification_flag_thumbnail.get_attribute('alt')
                
                
                driver.get(product_link)

                meta_title = findElement(driver,By.NAME,'title').get_attribute('value')
                meta_keywords = findElement(driver,By.NAME,'keywords').get_attribute('value')
                meta_description = findElement(driver,By.NAME,'description').get_attribute('value')

                product_header_copy = findElement(driver,By.CLASS_NAME,'product-header-copy')
                long_name = findElement(product_header_copy,By.TAG_NAME,'h1').text
                intro = findElement(product_header_copy,By.TAG_NAME,'p').text

                product_certifications = findElement(product_header_copy,By.CLASS_NAME,'product-certifications')
                product_certifications_flag = findElements(product_certifications,By.TAG_NAME,'img')
                product_certifications_flag = [item.get_attribute('src') for item in product_certifications_flag]

                product_header_img = findElement(driver,By.CLASS_NAME,'product-header-img')
                image_link = findElement(product_header_img,By.TAG_NAME,'img').get_attribute('src')

                tabs = findElements(driver,By.CLASS_NAME,'tab-pane')
                nav_tabs = findElements(findElement(driver,By.CLASS_NAME,'nav-tabs'),By.TAG_NAME,'a')
                tab_combine = zip(nav_tabs,tabs)
                long_desc = []
                for nav,tab in tab_combine:
                    nav.click()
                    h3 = findElement(tab,By.TAG_NAME,'h3').text
                    long_desc.append(findElement(tab,By.TAG_NAME,'ul').get_attribute('outerHTML'))
                    print('*'*100)

                product_list = [short_name,short_desc,image_link_thumbnail,slug,category_name,meta_title,meta_keywords,meta_description,rating,certification_flag_thumbnail,long_name,intro,product_certifications_flag,image_link,long_desc]
                # product_df = product_df.append(pd.Series(product_list,index=product_df.columns),ignore_index=True)
                product_df = pd.concat([product_df,pd.DataFrame([product_list],columns=product_df.columns)],ignore_index=True)
                print(product_list)
                product_df.to_csv('../data/final/product_details_v1.csv',index=False)

                print('='*50)
                driver.back()
        driver.back()
