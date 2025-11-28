import json
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd

# 設定中文字型（微軟正黑體）
plt.rcParams['font.family'] = font_manager.FontProperties(fname=r"C:\Windows\Fonts\msjh.ttc").get_name()
plt.rcParams['axes.unicode_minus'] = False  # 避免負號顯示錯誤

import os
os.chdir(r"C:\Users\ray5547c\Desktop\專案\全臺各級學校\大專院校")

# ---------------------------
# 讀取資料
# ---------------------------
# while True:
#     try:
#         v = int(input('輸入版本 v='))
#         # 讀取 JSON
#         with open(fr".\全臺工業區_v{v}.json", 'r', encoding='utf-8') as f:
#              data = json.load(f)
#         break
#     except:
#         print('輸入錯誤，請重新輸入')
#         
df_collage = pd.read_excel(r"C:\Users\ray5547c\Desktop\專案\全臺各級學校\大專院校\GeoJson\114學年_大專校院_v4.xlsx")
# ---------------------------
# 起始筆數
# ---------------------------
# position = input("輸入開始筆數: ")
# try:
#     position = int(position)
# except ValueError:
#     position = 0


# 假設 df_collage 已經整理好，經緯度欄位名稱以 '經緯度1', '經緯度2', ... 命名
coord_cols = [col for col in df_collage.columns if col.startswith('經緯度')]

for idx in range(len(df_collage)):
    row = df_collage.loc[idx]
    school_name = row['學校名稱']
    geom_type = row['範圍圖形']  # Polygon 或 MultiPolygon

    # 取出非空經緯度
    coords_str = row[coord_cols].dropna().tolist()

    # 如果沒有經緯度就跳過
    if not coords_str:
        continue

    plt.figure(figsize=(8, 8))
    plt.xlabel('經度')
    plt.ylabel('緯度')
    plt.title(f'{school_name} 範圍地圖')

    # MultiPolygon 處理方式：依照 ',' 分隔經緯度
    if geom_type == 'MultiPolygon':
        colors = ['#00fa9a', '#ffa500', '#1e90ff', '#ff69b4']
        poly_idx = 0
        temp_lon, temp_lat = [], []

        for c in coords_str:
            lng, lat = map(float, c.split(','))
            temp_lon.append(lng)
            temp_lat.append(lat)

            # 如果閉合，畫圖並清空暫存
            if len(temp_lon) > 2 and temp_lon[0] == temp_lon[-1] and temp_lat[0] == temp_lat[-1]:
                plt.plot(temp_lon, temp_lat, '-', color=colors[poly_idx % len(colors)])
                poly_idx += 1
                temp_lon, temp_lat = [], []

        # 畫最後一段（如果還有剩下的）
        if temp_lon:
            plt.plot(temp_lon, temp_lat, '-', color=colors[poly_idx % len(colors)])

    elif geom_type == 'Polygon':
        lon = [float(c.split(',')[0]) for c in coords_str]
        lat = [float(c.split(',')[1]) for c in coords_str]
        lon.append(lon[0])
        lat.append(lat[0])
        plt.plot(lon, lat, 'r-')

    plt.grid(True)
    plt.show()

