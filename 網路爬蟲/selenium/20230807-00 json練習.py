from selenium import webdriver
from selenium.webdriver.common.by import By

# 使用 Chrome 的 WebDriver
browser = webdriver.Chrome()

# 開啟 Google 首頁
browser.get("https://www.google.com.tw/maps/search/%E5%8F%B\
0%E5%8C%97%E6%8D%B7%E9%81%8B/@24.9969125,121.4830862,13.75z?hl=zh-TW&entry=ttu")

# 尋找網頁中的搜尋框
# inputElement = browser.find_element(By.CLASS_NAME, "gLFyf")

# 在搜尋框中輸入文字
# inputElement.send_keys("台北捷運圖 google map")

# 送出搜尋
# inputElement.submit()


