import pandas as pd
import openpyxl
import re

# -------------------------------
# 讀取資料
# -------------------------------
df_index = pd.read_csv(
    r"/Users/ray/Desktop/全臺各級學校/全臺各級學校_經緯度_v2.csv",
    low_memory=False
)
df_collage = pd.read_excel(
    r"/Users/ray/Desktop/全臺各級學校/大專院校/114學年_大專校院_v1.xlsx"
)

# 初始化新欄位
df_collage['範圍圖形'] = ''

# 只取大專院校資料
df_index_collage = df_index[df_index['學級'] == '大專院校']

# 建立空 list 儲存所有 matches
all_matches = []




for i in range(len(df_collage)):

    school_name = df_collage.loc[i, '學校名稱']

    # 找出所有名稱包含該學校的列
    matches = df_index_collage[df_index_collage['學校名稱'].str.contains(school_name, na=False, case=False)]

    # 如果有找到資料就加入 list
    if not matches.empty:
        all_matches.append(matches)

    # 移除已加入的經緯度列，避免重複匹配
    mask = df_index_collage['學校名稱'].str.contains(school_name, na=False)
    df_index_collage = df_index_collage[~mask].reset_index(drop=True)

    # 將所有 matches 合併成一個 DataFrame
    df_all_matches = pd.concat(all_matches, ignore_index=True)

def merge_school_rows(df, base_name_col='學校名稱', latlon_prefix='經緯度', shape_col='範圍圖形'):
    merged_rows = [] # 初始化列表
    # 去掉尾數數字取得  base names
    school_names = df[base_name_col].astype(str)
    base_names = set(re.sub(r'\d+$', '', name) for name in school_names)


    for base_name in base_names:
        # 主列：完全等於 base_name
        main_candidates = df[df[base_name_col] == base_name]

        # 衍生列：名稱後面跟數字
        pattern = f"^{re.escape(base_name)}\\d+$"
        derived_rows = df[df[base_name_col].str.match(pattern)].sort_index()

        # 選主列或第一衍生列
        if not main_candidates.empty:
            main_row = main_candidates.iloc[0].copy()
        elif not derived_rows.empty:
            main_row = derived_rows.iloc[0].copy()
            derived_rows = derived_rows.iloc[1:]
        else:
            continue


        if len(derived_rows) >= 1:
            main_row[shape_col] = 'MultiPolygon'
            
        latlon_cols = [col for col in df.columns if col.startswith(latlon_prefix)]
        existing_indices = []

        for col in latlon_cols:
                if col in main_row and pd.notna(main_row[col]):
                    m = re.search(r'(\d+)$', col)
                    if m:
                        existing_indices.append(int(m.group(1)))
        next_index = max(existing_indices) + 1 if existing_indices else 0
        for _, row in derived_rows.iterrows():
            for col in latlon_cols:
                value = row.get(col)
                if pd.notna(value):
                    main_row[f"{latlon_prefix}{next_index}"] = value
                    next_index += 1

        merged_rows.append(main_row)
    # 合併成 DataFrame
    return pd.DataFrame(merged_rows)

# 使用函數
df_merged = merge_school_rows(df_all_matches)
df_merged

# 檢查學校名稱還有誰有數字
df_with_numbers = df_merged[df_merged['學校名稱'].str.contains(r'\d', regex=True)]
df_with_numbers['學校名稱']

df_merged['代碼'] = None
df_merged['公/私立'] = None
df_merged['電話'] = None
df_merged['學校網址'] = None
df_merged['體系別'] = None

for _, row in df_collage.iterrows():
    base = row['學校名稱']
    type= row['公/私立']
    code = row['代碼']
    phone = row['電話']
    url = row['學校網址']
    system = row['體系別']
    
    # 前綴比對：all_matches.school_name 有出現 base 
    mask = df_merged['學校名稱'].str.contains(base, na=False)
    df_merged.loc[mask, '公/私立'] = type
    df_merged.loc[mask, '代碼'] = code
    df_merged.loc[mask, '電話'] = phone
    df_merged.loc[mask, '學校網址'] = url
    df_merged.loc[mask, '體系別'] = system 
    
# 檢查是否有沒有匹配到的資料
df_merged[df_merged['代碼'].isna()]

# 欄位排序
front_cols = ['代碼', "縣市名稱", '學校名稱', '學級', '公/私立', '電話', '學校網址', '體系別', '測製年月', 
              '範圍圖形', '中心經度', '中心緯度']

latlon_cols = [col for col in df_merged.columns if col.startswith('經緯度')]

new_order = front_cols + latlon_cols
df_merged = df_merged[new_order]
df_merged = df_merged.sort_values(by='代碼').reset_index(drop=True)

df_merged.columns
df_collage.columns


# 找出 df_collage 中代碼不在 df_merged 的列
missing_rows = df_collage[~df_collage['代碼'].isin(df_merged['代碼'])]
all_cols = df_merged.columns

# 如果經緯度欄位在 df_merged 中不存在，可以先補空值
latlon_cols = [col for col in df_merged.columns if col.startswith('經緯度')]
for col in all_cols:
    if col not in missing_rows.columns:
        missing_rows[col] = None

# 調整欄位順序一致
missing_rows = missing_rows[all_cols]

# 合併
df_merged = pd.concat([df_merged, missing_rows], ignore_index=True)

# 可以選擇依代碼排序
df_merged = df_merged[new_order]
df_merged = df_merged.sort_values(by='代碼').reset_index(drop=True)

df_merged.columns
df_merged.to_excel(
    r"/Users/ray/Desktop/114學年_大專校院_v2.xlsx",
    index=False
)

# df_index_collage.to_csv(r"C:\Users\ray5547c\Desktop\專案\全臺各級學校\大專院校\GeoJson\大專院校_經緯度_剩餘資料_v3.csv",
#                         encoding='utf-8-sig',
#                         index=False)
