#######################################################################################################################

# Following code is to get all the literature links along with relevent details to be stored in csv

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

literature_df = pd.DataFrame(columns=['documentType','productCategory','title','url'])

def check (i):
    if 'installation' in i:
        DocumentType = 'installation'
        productCateogry = i.replace('installation-','')
        return DocumentType,productCateogry
    elif 'product-brochure' in i:
        DocumentType = 'product-brochure'
        productCateogry = i.replace('product-brochure-','')
        return DocumentType,productCateogry
    elif 'specs' in i:
        DocumentType = 'specs'
        productCateogry = i.replace('specs-','')
        return DocumentType,productCateogry

source_url = 'https://www.airease.com/'

driver.get(source_url)

try:
    element = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,"onetrust-reject-all-handler"))
    )
    element.click()
except:
    pass

(findElement(driver,By.LINK_TEXT,'SUPPORT')).click()
(findElement(driver,By.LINK_TEXT,'PRODUCT LITERATURE')).click()

acc_body = findElements(driver,By.CLASS_NAME,'accordion-body')
# doc_category = [i for i in acc_body]
for i in acc_body:
    cateogry = i.get_attribute('id')
    DocumentType, productCateogry = check(cateogry)
    if productCateogry != 'installation' and productCateogry != 'product-brochure' and productCateogry != 'specs':
        links_raw = findElements(findElement(i,By.CLASS_NAME,'accordion-inner'),By.TAG_NAME,'a')
        titles = [item.get_attribute('text') for item in links_raw]
        links = [item.get_attribute('href') for item in links_raw]
        for title,link in zip(titles,links):
            literature_list = [DocumentType,productCateogry,title,link]
            literature_df = pd.concat([literature_df, pd.DataFrame([literature_list],columns=literature_df.columns)],ignore_index=True)
            print(literature_df)
# literature_df.to_csv('literature_details.csv',index=False)







