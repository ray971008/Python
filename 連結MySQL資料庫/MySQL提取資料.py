import pymysql
import pandas as pd

# 建立 MySQL 連線
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='你的密碼',
    database='cmdev',
    charset='utf8mb4'
)

# 讀取 emp 表
emp_df = pd.read_sql("SELECT * FROM emp", conn)
print("emp 表資料：")
print(emp_df)

# 讀取 dept 表
dept_df = pd.read_sql("SELECT * FROM dept", conn)
print("\ndept 表資料：")
print(dept_df)

# 關閉連線
conn.close()