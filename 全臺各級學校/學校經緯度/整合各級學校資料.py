import shapefile
from pyproj import Transformer
import pandas as pd
import os

os.chdir(r'C:\Users\ray5547c\Desktop\專案\全臺各級學校\學校經緯度')

# =============================
# 路徑設定
# =============================
# outlying 離島
# main 本島
shp_path_outlying = r".\各級學校範圍圖_119_1140801\campus_119_1140801.shp"
shp_path_main= r".\各級學校範圍圖_121分帶\campus_121_1141107.shp"

def change_shp_to_df(shp_path,EPSG_code):
    # =============================
    # 1. 讀取 shapefile
    # =============================
    sf = shapefile.Reader(shp_path, encoding="utf-8")

    records = sf.records()
    fields = [f[0] for f in sf.fields[1:]]
    df = pd.DataFrame(records, columns=fields)

    shapes = sf.shapes()

    # =============================
    # 2. 建立座標轉換器 (EPSG:3825 → EPSG:4326)
    # =============================
    transformer = Transformer.from_crs(f"EPSG:{str(EPSG_code)}", "EPSG:4326", always_xy=True)

    def convert_geometry(shape):
        """將 polygon / polyline 座標轉成 WGS84"""
        converted = []
        for x, y in shape.points:
            lon, lat = transformer.transform(x, y)
            converted.append([lon, lat])
        return converted

    # 幾何轉換
    df["geometry_wgs84"] = [convert_geometry(shape) for shape in shapes]

    # 若想取中心點
    def get_centroid(points):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        return sum(xs)/len(xs), sum(ys)/len(ys)

    df["lon"] = df["geometry_wgs84"].apply(lambda pts: get_centroid(pts)[0])
    df["lat"] = df["geometry_wgs84"].apply(lambda pts: get_centroid(pts)[1])

    # ============================================================
    # 1. 刪除欄位
    # ============================================================
    df = df.drop(columns=["LAYER", "YEAR","ID"], errors="ignore")

    # ============================================================
    # 2. 欄位重新命名
    # ============================================================
    df = df.rename(columns={
        "COUNTY": "縣市名稱",
        "BLOCKNAME": "學校名稱",
        "MDATE": "測製年月",
        "BLOCKTYPE": "範圍圖形",
        "lon": "中心經度",
        "lat": "中心緯度",
        "geometry_wgs84": "經緯度"
    })
    df['學級']=''
    df['範圍圖形']='Polygon'
    # ============================================================
    # 3. 將經緯度拆成 經緯度1、經緯度2、… 欄位
    # ============================================================
    # 找出最大 polygon 長度
    max_len = df["經緯度"].apply(len).max()

    coord_cols = []
    for i in range(max_len):
        col_name = f"經緯度{i+1}"
        coord_cols.append(col_name)
        df[col_name] = df["經緯度"].apply(
            lambda coords: f"{coords[i][0]},{coords[i][1]}" if i < len(coords) else None
        )

    # 拆完後刪除原本欄位
    df = df.drop(columns=["經緯度"])

    # ============================================================
    # 4. 欄位順序：前面固定，其餘經緯度欄位依序排列
    # ============================================================
    base_order = [
        "縣市名稱",
        "學校名稱",
        '學級',
        "測製年月",
        "範圍圖形",
        "中心經度",
        "中心緯度"
    ]

    df = df[base_order + coord_cols]
    df = df.applymap(lambda x: x.replace(" ", "") if isinstance(x, str) else x)
    return df

# ============================================================
# 5. 依照指定順序排列「縣市名稱」
# ============================================================

df_main = change_shp_to_df(shp_path_main,3826)
ordered_areas = [
    '臺北市', '新北市', '基隆市', '桃園市', '新竹縣',
    '苗栗縣', '臺中市', '彰化縣', '南投縣', '雲林縣',
    '嘉義縣', '臺南市', '高雄市', '屏東縣',
    '宜蘭縣', '花蓮縣', '臺東縣'
]

df_main["縣市名稱"] = pd.Categorical(df_main["縣市名稱"], categories=ordered_areas, ordered=True)
df_main = df_main.sort_values("縣市名稱").reset_index(drop=True)
df_main.iloc[0,0:40]

df_outlying = change_shp_to_df(shp_path_outlying,3825)
df_outlying.iloc[0,0:50]


# ============================================================
# 6. 合併資料
# ============================================================
# 找出 df_main 的所有欄位
all_cols = df_main.columns

# 將 df_outlying 欄位對齊，如果缺少欄位就補 NaN
df_outlying = df_outlying.reindex(columns=all_cols)

# 合併
df_combined = pd.concat([df_main, df_outlying], ignore_index=True)

df = df_combined.copy()
for i in range(len(df)):
    print(f'完成 第{i}筆')
    name = str(df.loc[i, '學校名稱'])
    if '國民小學' in name:
        grade = '國小'
    elif '國民中學' in name:
        grade = '國中'
    elif (('高級中學' in name) or ('職業學校' in name)) and '附設' not in name:
        grade = '高中'
    elif ('大學' in name) and ('附設' not in name):
        grade = '大專院校'
    else:
        grade = ''
    df.loc[i,'學級'] = grade
df.to_csv('全臺各級學校_經緯度_v1.csv',encoding='utf-8-sig',index=False)

import gc

# 刪掉不再需要的 DataFrame
del df_main
del df_outlying
del df_combined
del df
# 強制垃圾回收
gc.collect()