from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import base64
import pytesseract

# 建立 Service 物件
service = Service(ChromeDriverManager().install())
# Service 在做什麼？
# 例如 ChromeDriverManager().install() 會下載好 chromedriver，然後傳回一個路徑。
# Service 負責接收這個路徑，並準備好啟動它。

# 啟動 Chrome
browser = webdriver.Chrome(service=service)

# 打開網址
browser.get("https://www.mvdis.gov.tw/m3-emv-vil/vil/penaltyQueryPay#gsc.tab=0")

# 帳號密碼位置
id = browser.find_element(By.XPATH,'//input[@type="text"][@name="uid"]')
password = browser.find_element(By.XPATH,'//input[@name="birthday"]')
key = browser.find_element(By.XPATH, "//input[@name='validateStr']")

# 驗證碼圖片轉換文字
img_base64 = browser.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);    
    """, browser.find_element(By.XPATH, "//*[@align='left']/img"))

from PIL import Image
from io import BytesIO 
img_data = base64.b64decode(img_base64)

# 開啟圖片
img = Image.open(BytesIO(img_data))
#img.show()

# 如果系統有安裝 tesseract，直接辨識
text = pytesseract.image_to_string(img, config="--psm 8 --oem 3")
print("辨識結果：", text.strip())


# 將圖片轉成黑白，去掉背景干擾
import base64
from PIL import Image
from io import BytesIO
import numpy as np
import cv2

# 1. base64 轉 bytes
img_data = base64.b64decode(img_base64)

# 2. bytes 轉 PIL Image
img = Image.open(BytesIO(img_data))
#img.show()  # 確認圖片是否正確

# 3. PIL -> OpenCV 格式
img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# 4. 灰階
gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

# 5. 二值化
_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

# 6. PIL 轉回 image（給 pytesseract 使用）
img_processed = Image.fromarray(thresh)
img_processed.show()

text = pytesseract.image_to_string(img_processed , config="--psm 8 --oem 3")
text = text.replace(' ', '')   # 移除空格
text = text.replace('\n', '')  # 移除換行
print("辨識結果：", text)

time.sleep(2)
id.send_keys('A127933214')
time.sleep(1)
password.send_keys('861008')
time.sleep(1)
key.send_keys('text')
time.sleep(1)
key.submit()
