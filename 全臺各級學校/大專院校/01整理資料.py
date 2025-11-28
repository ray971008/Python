import pandas as pd
import openpyxl
df = pd.read_excel(
    r"C:\Users\ray5547c\Desktop\專案\全臺各級學校\大專院校\大專校院名單.xlsx",
    header=2,  # 將第 2 列視為欄位名稱
    dtype={"代碼": str}
)

import re

# 1. 移除舊的「縣市名稱」欄位
df = df.drop(columns=["縣市名稱"])

# 2. 將 Unnamed: 4 改名為「縣市名稱」
df = df.rename(columns={"Unnamed: 4": "縣市名稱","網址":"學校網址"})

# 3. 去除所有 [數字]
df = df.replace(r"\[\d+\]", "", regex=True)

# 4. 去除字串前後空白（避免變成 ' 臺北市' 這類）
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.to_excel(r'C:\Users\ray5547c\Desktop\專案\全臺各級學校\大專院校\114學年_大專校院_v1.xlsx',index=False)

