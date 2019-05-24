import time
from selenium import webdriver
URLS = ("https://www.google.com", "http://www.yahoo.com", "http://www.bing.com")
 
PATH_TO_DRIVER = 'C:/Users/Henok/Downloads/chromedriver_win32 (1)/chromedriver.exe'
browser = webdriver.Chrome(PATH_TO_DRIVER)
browser.set_window_position(0,0)
# for url in URLS:
#     browser.get(url)
#     time.sleep(5)

browser.get('http://46.101.144.34:9000/bin/counter/')