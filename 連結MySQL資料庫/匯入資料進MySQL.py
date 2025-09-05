from sqlalchemy import create_engine
import pandas as pd

# 1️⃣ 設定 MySQL 帳號密碼與資料庫
root = 'root'                      # 使用的 MySQL 帳號，可依情況修改
password = 'ray809255'             # MySQL 密碼，請改成你的密碼
host = 'localhost'                 # MySQL 主機位置
                                   # localhost: 本機
                                   # 127.0.0.1: 本機 TCP/IP
                                   # 遠端 IP 或域名: 例如 192.168.1.100 或 db.example.com
port = 3306                        # MySQL 端口，預設為 3306，可依伺服器設定修改
database = 'threads'               # 要連線的資料庫名稱
charset = 'utf8mb4'                # 資料庫字元編碼，可修改，例如 'utf8' 或 'latin1'
                                   # utf8mb4: 支援中文、英文、emoji 以及特殊符號，避免亂碼


# 1️⃣ 先連到 MySQL 伺服器，不指定資料庫(若已存在資料庫則跳過)
engine = create_engine(
    f'mysql+pymysql://{root}:{password}@{host}:{port}/?charset={charset}'
)

# 1️⃣ 創建資料庫（若已存在則跳過）
# =========================
database_name = database
with engine.connect() as conn:
    conn.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print(f"資料庫 {database_name} 已建立或已存在")


# 1️⃣ 連線到 MySQL threads 資料庫
engine = create_engine(
    f'mysql+pymysql://{root}:{password}@{host}:{port}/{database}?charset={charset}'
)

# 2️⃣ 讀 CSV
df = pd.read_csv('*.csv')

# 3️⃣ 匯入 MySQL
df.to_sql('*', con=engine, if_exists='replace', index=False) #若存在 table 則取代
engine.dispose()  # 關閉所有連線池的連線