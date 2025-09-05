from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # 瀏覽器選項設定模組
from selenium.webdriver.common.by import By

url = "https://www.facebook.com/"

driver = webdriver.Chrome()
# 設定 chrome

driver.get(url)

id = driver.find_element(By.XPATH,"//input[@type='text'][@class='inputtext _55r1 _6luy']")
password = driver.find_element(By.XPATH,"//input[@type='password'][@class='inputtext _55r1 _6luy _9npi']")

# 送資料進入網頁
id.send_keys("0905809255")
password.send_keys("ray809255")

# 送出資料
password.submit()


# login = driver.find_element(By.XPATH,"//button[@class='_42ft _4jy0 _6lth _4jy6 _4jy1 selected _51sy'][@name='login']")
# login.click()