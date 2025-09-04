university = ['台大','台大','台大','陽明','陽明','陽明'
              ,'清大','清大','清大','交大','交大','交大']
sub = ['醫學','工程','農學','醫學','工程','農學',
       '醫學','工程','農學','醫學','工程','農學']
ord = [1,1,1,2,None,None,None,2,None,None,3,None]

import pandas as pd
data = {'大學':university ,
        '專業':sub,
        '排名':ord}
df=pd.DataFrame(data)

df.loc[0:4]
df.loc[:,['大學','專業']]

df.iloc[0:4]
df.iloc[0:4,2]
df.iloc[0:4,[0,1,2]]



# 相同主鍵合併資料 join 函數
df1 = pd.DataFrame({'key': ['A', 'B', 'C', 'D'], 'value1': [1, 2, 3, 4]})
df2 = pd.DataFrame({'key': ['B', 'D', 'E', 'F'], 'value2': [5, 6, 7, 8]})

merged_df_inner = pd.merge(df1, df2, on='key', how='inner')
print("Inner Join:\n", merged_df_inner)

merged_df_inner = pd.merge(df1, df2, on='key', how='left')
print("Inner Join:\n", merged_df_inner)

merged_df_inner = pd.merge(df1, df2, on='key', how='right')
print("Inner Join:\n", merged_df_inner)

merged_df_outer = pd.merge(df1, df2, on='key', how='outer')
print("\nOuter Join:\n", merged_df_outer)

# 第二種方法
df1 = pd.DataFrame({'value1': [1, 2, 3]}, index=['A', 'B', 'C'])
df2 = pd.DataFrame({'value2': [4, 5, 6]}, index=['B', 'C', 'D'])

joined_df = df1.join(df2)
print("Joined DataFrame:\n", joined_df)

joined_df_inner = df1.join(df2, how='inner')
print("\nInner Joined DataFrame:\n", joined_df_inner)



# 縱向合併 concat函數
df1 = pd.DataFrame({'Name': ['Alice', 'Bob'], 'Age': [25, 30]})
df2 = pd.DataFrame({'Name': ['Charlie', 'David'], 'Age': [35, 40]})

print(df1)
print(df2)

# Concatenate vertically (stacking rows)
concatenated_rows = pd.concat([df1, df2])
print("Concatenated Rows:\n", concatenated_rows)


# 橫向合併新增欄位 concat函數
df3 = pd.DataFrame({'City': ['New York', 'Los Angeles']})
df4 = pd.DataFrame({'Salary': [70000, 80000]})

concatenated_cols = pd.concat([df3, df4], axis=1)
print("\nConcatenated Columns:\n", concatenated_cols)
