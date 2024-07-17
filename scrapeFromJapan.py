from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
chrome_options=Options()
chrome_options.add_argument("--headless=new")
user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')

try:
    with open('fjplinks.json') as json_file:
        links=json.load(json_file)
except:
    links=dict()

def getItem(url):
    driver=webdriver.Chrome(
        options=chrome_options
                            )
    driver.get(url)
    
    try:
        wait=WebDriverWait(driver,timeout=10)
        wait.until(lambda c: 'swiper-slide swiper-slide-active' in driver.page_source)
        
    finally:
        html=driver.page_source
        driver.quit()
    soup=BeautifulSoup(html,'html.parser')
    name=soup.find(class_='text-lg lg:text-2xl mb-2 leading-normal')
    itemName=name.string
    itemPrice=0
    prices=soup.find_all(class_='text-sm text-grey')
    for price in prices:
        if 'yen' in price.string:
            itemPrice=price.string[1:price.string.index(' ')].replace(',','')
    imageCarousel=soup.find(class_='swiper-wrapper')
    images=list(map(lambda x: x['src'],imageCarousel.find_all('img')))
    #itemDescription=soup.find(class_='leading-loose').string  
    return {'images':images,'price':itemPrice,'name':itemName.encode('utf-8')}
    
def getPage(url):
    driver=webdriver.Chrome(
        options=chrome_options
                            )
    driver.get(url)
    
    try:
        wait=WebDriverWait(driver,timeout=10)
        wait.until(lambda c: 'shop-list flex justify-start flex-wrap' in driver.page_source)
        
    finally:
        html=driver.page_source
        driver.quit()
    soup=BeautifulSoup(html,'html.parser')
    
    return soup.find_all("a", href=re.compile(r'(?:/japan/en/special|/japan/en/auction)'))


def getTerm(term):
    items=getPage('https://www.fromjapan.co.jp/japan/en/item/search/'+term.replace(' ','+')+'/Al_11_Yh_RaSuBpRmMrMv_N_N_0A00ja00_N/')
    l=[]
    for item in items:
        link='https://www.fromjapan.co.jp'+item['href']
        if link not in l:
            l.append(link)
    return l
