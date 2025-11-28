import pandas as pd
import re
import json
import os
os.chdir(r'C:\Users\ray5547c\Desktop\專案\全臺各級學校\GeoJson')
while True:
    try:
        v = int(input('輸入版本 v='))
        df = pd.read_csv(rf".\全臺各級學校_經緯度_v{v}.csv", low_memory=False)
        break

    except:
        print('輸入錯誤，請重新輸入')
        continue

true_df = df[(df['範圍圖形'] == 'Polygon') | (df['範圍圖形'] == 'MultiPolygon') ]

# 儲存所有 Feature
features = []

for idx, row in true_df.iterrows():
    name = row['學校名稱']
    shape_type = str(row['範圍圖形']).strip()  # Polygon 或 MultiPolygon

    # --- 收集經緯度 ---
    latlng_groups = []  # 用於 MultiPolygon（多組）
    latlng = []         # 單一 Polygon 用

    for i in range(1, 12000):
        key = f'經緯度{i}'
        if key not in row:
            break
        text = str(row.get(key, '')).strip()
        if not text or text.lower() == 'nan':
            break

        match = re.match(r'\s*([-\d.]+)\s*,\s*([-\d.]+)\s*', text)
        if match:
            lng = float(match.group(1))
            lat = float(match.group(2))
            latlng.append([lng, lat])

        # MultiPolygon 分段判斷（可依 note 或座標重複判斷）
        # 若遇到重複的起點，可視為一個新多邊形的開頭
        if shape_type == 'MultiPolygon' and len(latlng) > 3:
            if latlng[-1] == latlng[0]:
                latlng_groups.append(latlng)
                latlng = []

    # 最後一段也補上
    if latlng:
        # 確保 Polygon 閉合
        if latlng[0] != latlng[-1]:
            latlng.append(latlng[0])
        if shape_type == 'MultiPolygon':
            latlng_groups.append(latlng)

    # --- 中心點 ---
    center = [float(row['中心經度']), float(row['中心緯度'])]

    # --- 建立 Feature ---
    if shape_type == 'Polygon' and latlng:
        features.append({
            "type": "Feature",
            "properties": {
                "name": name,
                "stroke": "#FF359A",
                "stroke-width": 5,
                "fill": "#FFFFFF",
                "fill-opacity": 0
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [latlng]
            }
        })

    elif shape_type == 'MultiPolygon' and latlng_groups:
        features.append({
            "type": "Feature",
            "properties": {
                "name": name,
                "stroke": "#9932cc",
                "stroke-width": 5,
                "fill": "#FFFFFF",
                "fill-opacity": 0
            },
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [[group] for group in latlng_groups]
            }
        })

    # --- 中心點標記 ---
    features.append({
        "type": "Feature",
        "properties": {
            "name": name,
            "marker-color": "#FF9224",
            "marker-symbol": "circle"
        },
        "geometry": {
            "type": "Point",
            "coordinates": center
        }
    })

# --- 輸出整體 FeatureCollection ---
geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

# 輸出成 txt 檔
with open(rf".\全臺各級學校_經緯度_v{v}.json", "w", encoding="utf-8") as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=2)

print(f"✅ 已成功輸出 全臺各級學校_經緯度_v{v}.json")

