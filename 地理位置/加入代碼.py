import re
import pandas as pd

df = pd.read_csv(r'縣市鄉鎮區代碼.csv', encoding="utf-8-sig")
df2 = pd.read_csv(r'商圈.csv', encoding="utf-8-sig")

namelst=list(df2['名稱']) # 商區名稱 
addresslst = list(df2['地址'])
lat = list(df2['lat'])
lng = list(df2['lng'])
note = list(df2['有疑慮備註'])

citylst=[] # 縣市
city_codelst=[] # 縣市代碼
districtlst=[] # 鄉鎮區
district_codelst=[] # 鄉鎮區代碼

for k in addresslst:
    # 先判斷「縣」的情況
    if re.match(r'.+縣', k):
        city_match = re.match(r'(.+?縣)\s*(.+?[鄉鎮市])', k)
    elif re.match(r'.+市', k):
        city_match = re.match(r'(.+?市)\s*(.+?區)', k)
    # 再判斷「市」的情況
    else:
        city_match = None

    if city_match:
        city = city_match.group(1)
        district = city_match.group(2)
        citylst.append(city)
        districtlst.append(district)
    else:
        print(f"無法匹配的地址: {k}")
        
    # 縣市代碼搜尋
    city_code = df[df['縣市名稱'] == city]['縣市代碼'].iloc[0]
    city_codelst.append(city_code)

    district_code_series = df[(df['縣市名稱'] == city) & (df['鄉鎮區名稱'] == district)]['鄉鎮區代碼']
    if not district_code_series.empty:
        district_code = district_code_series.iloc[0]
        district_codelst.append(district_code)
    else:
        district_code_series = df[(df['縣市名稱'] == city) & (df['鄉鎮區名稱'] == district+'區')]['鄉鎮區代碼'].iloc[0]
        district_codelst.append(district_code)

df2['縣市']=citylst
df2['鄉鎮區']=districtlst
df2['縣市代碼']=city_codelst
df2['鄉鎮區代碼']=district_codelst
df2 = df2[['縣市', '鄉鎮區', '縣市代碼', '鄉鎮區代碼', '名稱', '地址','lat','lng','有疑慮備註']]

df2.to_csv(r'商圈.csv', index=False, encoding="utf-8-sig")