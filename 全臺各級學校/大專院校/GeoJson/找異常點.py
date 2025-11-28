
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
df_collage = pd.read_excel(r"C:\Users\ray5547c\Desktop\專案\全臺各級學校\大專院校\GeoJson\114學年_大專校院_v11.xlsx")

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

# school_name = str(input('輸入學校名稱:'))
school_name = '國防醫學大學'
start, end =960, 969 # 指定要標藍色的範圍（從1開始）

# row = df_collage[df_collage['學校名稱']==school_name]
idx = df_collage.index.get_loc(df_collage[df_collage['學校名稱'] == school_name ].index[0])

row = df_collage.loc[idx]

geom_type = row['範圍圖形']  # Polygon 或 MultiPolygon
# 取出非空經緯度
coords_str = row[coord_cols].dropna().tolist()

start_idx = max(start-1, 0)
end_idx = min(end, len(coords_str))


plt.figure(figsize=(8, 8))
plt.xlabel('經度')
plt.ylabel('緯度')
plt.title(f'{school_name} 範圍地圖')

# MultiPolygon 處理方式：依照 ',' 分隔經緯度
if geom_type == 'MultiPolygon':
    colors = ['#00fa9a', '#ffa500', '#1e90ff', '#ff69b4']
    poly_idx = 0
    temp_lon, temp_lat = [], []
    start_idx_poly = 0 # 記錄每塊 polygon 的起始 index

    for i, c in enumerate(coords_str):
        lng, lat = map(float, c.split(','))
        temp_lon.append(lng)
        temp_lat.append(lat)
        # 閉合判斷
        if len(temp_lon) > 2 and temp_lon[0] == temp_lon[-1] and temp_lat[0] == temp_lat[-1]:
            end_idx_poly = i
            print(f"Polygon {poly_idx+1}: 經緯度{start_idx_poly+1} ~ 經緯度{end_idx_poly+1}")
            plt.plot(temp_lon, temp_lat, '-', color=colors[poly_idx % len(colors)])
            poly_idx += 1
            temp_lon, temp_lat = [], []
            start_idx_poly = i + 1

    # 畫最後一段（如果還有剩下的）
    if temp_lon:
        end_idx_poly = len(coords_str) - 1 
        print(f"Polygon {poly_idx+1}: 經緯度{start_idx_poly+1} ~ 經緯度{end_idx_poly+1}")
        plt.plot(temp_lon, temp_lat, '-', color=colors[poly_idx % len(colors)])

elif geom_type == 'Polygon':
    print(f"經緯度1 ~ 經緯度{len(coords_str)}")
    lon = [float(c.split(',')[0]) for c in coords_str]
    lat = [float(c.split(',')[1]) for c in coords_str]
    lon.append(lon[0])
    lat.append(lat[0])
    plt.plot(lon, lat, 'r-')


# 畫藍色範圍 
blue_lon = [float(coords_str[i].split(',')[0]) for i in range(start_idx, end_idx)]
blue_lat = [float(coords_str[i].split(',')[1]) for i in range(start_idx, end_idx)]
plt.scatter(blue_lon, blue_lat, color='b', s=50, zorder=5)  # s=點大小, zorder=疊在上面

plt.grid(True)
plt.show()


