from selenium import webdriver
import time
# from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()

browser.get("https://www.ptt.cc/bbs/joke/index8385.html")

for i in range(3):
    print('第',i+1,'頁')
    # browser.find_element[s] 後面加s代表找多個
    title = browser.find_elements(By.CLASS_NAME,'title')
    for i in title:
        ans = i.text
        print(ans)
    print()
    time.sleep(3)
    inputElement = browser.find_element(By.LINK_TEXT,"‹ 上頁")
    # 定位.click() 控制滑鼠點下去
    inputElement.click()


    




