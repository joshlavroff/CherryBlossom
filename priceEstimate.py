from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import trim
import json
from selenium.webdriver.chrome.options import Options
chrome_options=Options()
chrome_options.add_argument("--headless=new")
user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')

try:
    with open('prices.json') as json_file:
        prices=json.load(json_file)
except:
    prices=dict()

def getAvgPrice(keyword,updateList=False):
    if keyword in prices and not updateList:
        return prices[keyword]
    
    url="https://www.grailed.com/shop"

    ser=Service("D:\chromedriver-win64\chromedriver.exe")
    driver=webdriver.Chrome(service=ser,options=chrome_options)
    driver.get(url)

    try:
        searchBox = driver.find_element(By.CLASS_NAME, "Form-module__input___mDyy5")
        searchButton = driver.find_element(By.XPATH, "//*[contains(text(),'Search')]")
        action = ActionChains(driver)
        action.click().perform()
        action.click().perform()
        searchBox.send_keys(keyword)
        action.move_to_element(searchButton).click().perform()
        driver.implicitly_wait(1)
        time.sleep(1)
        sortDrop=driver.find_element(By.CLASS_NAME,'ais-SortBy-select')
        sortSelect=select.Select(sortDrop)
        sortSelect.select_by_value('Listing_by_date_added_production')
        driver.implicitly_wait(1)
        time.sleep(1)
        soldButton=driver.find_element(By.ID,'sold-filter')
        #soldButton.click()
        # driver.implicitly_wait(5)
        # time.sleep(5)
        pri = driver.find_elements(By.CLASS_NAME, 'Money-module__root___jRyq5')
        total = 0
        print(len(pri))
        for p in pri:
            total += float(trim.trimStr(p.text[1:]))
        avg = round(total / (len(pri) - 3), 2)
        prices[keyword]=avg
        with open("prices.json", "w") as outfile: 
            json.dump(prices, outfile)
        return avg
    except Exception as e:
       print(e)
       return 0


def checkSoldListings(driver,action):
    try:
        showOnly = driver.find_element(By.XPATH, "//*[contains(text(),'Show Only')]")
        showOnly.click()
    except:
        driver.close()

    time.sleep(1)

    try:
        sold = driver.find_element(By.XPATH, "//*[contains(text(),'Sold')]")
        action.move_to_element(sold).click().perform()
        action.move_to_element(sold).click().perform()

    except:
        driver.close()

