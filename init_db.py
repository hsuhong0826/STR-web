import sqlite3

def init():
    conn = sqlite3.connect('sketch2real.db')
    c = conn.cursor()

    # 建立 users 表
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        name TEXT NOT NULL,
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    ''')

    # 建立 login_attempts 表（型別改為 DATETIME）
    c.execute('''
    CREATE TABLE IF NOT EXISTS login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        attempt_time DATETIME NOT NULL
    )
    ''')

    # 插入預設帳號（如果不存在才插入）
    default_users = [
        ('管理員', 'admin', 'admin'),
        ('林羿彣', 'eva900722', 'eva900722'),
        ('許振鴻', 'hong0826', 'hong0826')
    ]

    inserted = 0
    for name, username, password in default_users:
        c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if not c.fetchone():
            c.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)", (name, username, password))
            inserted += 1

    conn.commit()
    conn.close()

    print(f"[INIT] ✅ 資料庫初始化完成，共插入 {inserted} 筆預設帳號。")
