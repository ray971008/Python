
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
df_collage = pd.read_excel(r"C:\Users\ray5547c\Desktop\專案\全臺各級學校\大專院校\GeoJson\114學年_大專校院_v3.xlsx")

# school_name = str(input('輸入學校名稱:'))
school_name = '國防醫學大學'
start, end =123, 136 # 指定要標藍色的範圍（從1開始）

# 找出該學校的所有經緯度欄位
coord_cols = [col for col in df_collage.columns if col.startswith('經緯度')]
row_idx = df_collage[df_collage['學校名稱'] == school_name].index[0]

# 將經緯度值抓成列表
coords = df_collage.loc[row_idx, coord_cols].tolist()

# 刪除指定範圍 (start, end 從1開始)
start_idx = start - 1
end_idx = end   # end 索引為 Python list 需要 +1 已包含
del coords[start_idx:end_idx]

# 將列表補回 DataFrame，剩餘欄位設為 NaN
for i, col in enumerate(coord_cols):
    if i < len(coords):
        df_collage.at[row_idx, col] = coords[i]
    else:
        df_collage.at[row_idx, col] = pd.NA


# 或另存新檔
df_collage.to_excel(r"C:\Users\ray5547c\Desktop\專案\全臺各級學校\大專院校\GeoJson\114學年_大專校院_v4.xlsx", index=False)
