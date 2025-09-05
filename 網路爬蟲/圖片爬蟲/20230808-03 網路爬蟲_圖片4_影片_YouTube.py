# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 13:26:19 2023

@author: Admin
"""

from pytube import YouTube,Playlist
import time ,os

# youtube 播放清單
plist = Playlist('https://www.youtube.com/watch?v=kzdJkT4kp-A&list=PLR48NTfP0M0NCOpY1vsFa9OjUW0vBbvYf&index=2&ab_channel=Ayase%2FYOASOBI')

print(plist)

path = r'C:\2張家瑞\20230808\songs'
if not os.path.exists(path):
    os.mkdir(path)

for url in plist.video_urls:
    if url != 'https://www.youtube.com/watch?v=x8VYWazR5mE':
        yt = YouTube(url)
        print(yt.title,' 開始下載中...')
        # yt.streams.first().download(path) # 下載預設畫質(低畫質)
        yt.streams.filter().get_highest_resolution().download(path) #高畫質
        print('影片下載完成')
        print('停滯 10 秒')
        time.sleep(5)
        print()
        
    