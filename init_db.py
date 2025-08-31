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

    # 建立 login_attempts 表
    c.execute('''
    CREATE TABLE IF NOT EXISTS login_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        attempt_time TEXT NOT NULL
    )
    ''')

    # 插入預設帳號（只有在帳號不存在時才插入）
    default_users = [
        ('管理員', 'admin', 'admin'),
        ('林羿彣', 'eva900722', 'eva900722'),
        ('許振鴻', 'hong0826', 'hong0826')
    ]

    for name, username, password in default_users:
        c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if not c.fetchone():
            c.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)", (name, username, password))

    conn.commit()
    conn.close()
