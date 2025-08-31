# init_db.py
import sqlite3

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

# 插入預設使用者
c.executemany('''
INSERT INTO users (name, username, password) VALUES (?, ?, ?)
''', [
    ('管理員', 'admin', 'admin'),
    ('林羿彣', 'eva900722', 'eva900722'),
    ('許振鴻', 'hong0826', 'hong0826')
])

conn.commit()
conn.close()
