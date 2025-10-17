import pandas as pd
import mysql.connector
from mysql.connector import Error

# -----------------------------
# 1. CSV 檔案路徑
# -----------------------------
csv_file = '商圈1.csv'

# -----------------------------
# 2. 讀取 CSV
# -----------------------------
try:
    df = pd.read_csv(csv_file, encoding='utf-8-sig')
    print("CSV 讀取成功，資料筆數：", len(df))
except Exception as e:
    print("讀取 CSV 失敗：", e)
    exit(1)

# -----------------------------
# 3. 連線 MariaDB
# -----------------------------
host = '輸入ip'
port = 3306
user = '輸入使用者'
password = '輸入密碼'
database = '輸入資料庫名稱'

try:
    conn = mysql.connector.connect(
        host=host,              # 主機端對應 Docker 映射
        port=port,              # 端口
        user=user,              # 你的 MariaDB 帳號
        password=password,      # 你的 MariaDB 密碼
        database=database       # 你的資料庫名稱
    )
    conn = mysql.connector.connect(
        host=f'{host}',      # 主機端對應 Docker 映射
        port=f'{pprt}',
        user=f'{user}',           # 你的 MariaDB 帳號
        password=f'{password}',    # 你的 MariaDB 密碼
        database=f'{database}'        # 你的資料庫名稱
    )
    cursor = conn.cursor()
    print("成功連線 MariaDB！")
except Error as e:
    print("連線失敗：", e)
    exit(1)


# -----------------------------
# 4. 建立資料表（如果不存在）
# -----------------------------
create_table_sql = """
CREATE TABLE IF NOT EXISTS `商圈` (
    `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `縣市` VARCHAR(20) DEFAULT NULL,
    `鄉鎮區` VARCHAR(20) DEFAULT NULL,
    `縣市代碼` INT(20) DEFAULT NULL,
    `鄉鎮區代碼` INT(20) DEFAULT NULL,
    `名稱` VARCHAR(40) DEFAULT NULL,
    `地址` VARCHAR(60) DEFAULT NULL,
    `lat` DOUBLE DEFAULT NULL,
    `lng` DOUBLE DEFAULT NULL,
    `有疑慮備註` VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cursor.execute(create_table_sql)
print("資料表已建立或已存在。")

# -----------------------------
# 5. 將 CSV 寫入資料表
# -----------------------------
insert_sql = """
INSERT INTO 商圈
(縣市, 鄉鎮區, 縣市代碼, 鄉鎮區代碼, 名稱, 地址, lat, lng, 有疑慮備註)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for idx, row in df.iterrows():
    try:
        cursor.execute(insert_sql, (
            row.get('縣市'),
            row.get('鄉鎮區'),
            row.get('縣市代碼'),
            row.get('鄉鎮區代碼'),
            row.get('名稱'),
            row.get('地址'),
            row.get('lat'),
            row.get('lng'),
            row.get('有疑慮備註') if pd.notnull(row.get('有疑慮備註')) else ''
        ))
    except Exception as e:
        print(f"資料列 {idx} 寫入失敗：", e)

# -----------------------------
# 6. 提交變更 & 關閉連線
# -----------------------------
conn.commit()
cursor.close()
conn.close()
print("資料全部寫入完成！")