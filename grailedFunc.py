from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import trim
import json
import sys 
import priceEstimate

#print(priceEstimate.getAvgPrice('jordan 4 military blue'))
# enc=b'\xe7\xbe\x8e\xe5\x93\x81\xe2\x9c\xa8Chloe\xe3\x82\xaf\xe3\x83\xad\xe3\x82\xa8 / \xe3\x83\x91\xe3\x83\x87\xe3\x82\xa3\xe3\x83\xb3\xe3\x83\x88\xe3\x83\xb3 \xe3\x83\x9b\xe3\x83\xaf\xe3\x82\xa4\xe3\x83\x88'
# enc2='\xe7\xbe\x8e\xe5\x93\x81\xe2\x9c\xa8Chloe\xe3\x82\xaf\xe3\x83\xad\xe3\x82\xa8 / \xe3\x83\x91\xe3\x83\x87\xe3\x82\xa3\xe3\x83\xb3\xe3\x83\x88\xe3\x83\xb3 \xe3\x83\x9b\xe3\x83\xaf\xe3\x82\xa4\xe3\x83\x88'
# import chardet
# chardet.detect(enc)
# {'confidence': 0.505, 'encoding': 'utf-8'}
# #print(enc.decode(chardet.detect(enc)['encoding']).encode('unicode_escape'))
# print(enc2.encode('unicode_escape'))
teststring='abcdef'
print(teststring[3])