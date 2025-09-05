# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 15:28:38 2023

@author: Admin
"""

print('第 1 題')
import requests,os
os.chdir(r'C:\pictures')
url = 'https://b.share.photo.xuite.net/jameslee1960/1bacb49/10870478/505765243_m.jpg'

img = requests.get(url)
# print(img.content)
with open(r'C:\pictures\doggy.jpg','wb') as file:
    file.write(img.content)
    
# print()
    


    
    
    


