import pandas as pd
import os
os.chdir(r'C:\Users\ray5547c\Desktop\專案\全臺各級學校\GeoJson')
df=pd.read_csv(f'全臺各級學校_經緯度_v2.csv',low_memory=False)

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

    if grade in ['國小', '國中', '高中']:
        if '私立' in name:
            type = '私立'
        else:
            type = '公立'
    elif grade == '大學':
        if '國立' in name:
            type = '公立'
        else:
            type = '私立'
    else:
        type = ''
    df.loc[i,'公/私立']=type

df.to_csv('全臺各級學校_經緯度_v3.csv',index=False,encoding='utf-8-sig')

