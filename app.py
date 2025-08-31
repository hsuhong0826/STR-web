# ===================== 導入套件 =====================
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from datetime import datetime, timedelta
import sqlite3
import init_db

# ===================== 建立 Flask 應用 =====================
app = Flask(__name__)
app.secret_key = "hong0826"
CORS(app)

# ===================== 建立 SQLite 資料庫連線 =====================
def get_db_connection():
    conn = sqlite3.connect('sketch2real.db')
    conn.row_factory = sqlite3.Row  # 讓 cursor.fetchone() 可以像字典那樣取值
    return conn

# ===================== 註冊 API =====================
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        return jsonify({'msg': '帳號已存在'}), 400

    cursor.execute(
        "INSERT INTO users (name, username, password) VALUES (?, ?, ?)", 
        (name, username, password)
    )
    conn.commit()
    conn.close()
    return jsonify({'msg': '註冊成功'})

# ===================== 登入 API =====================
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    # 查詢 10 分鐘內登入失敗次數
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    cursor.execute(
        "SELECT COUNT(*) AS fail_count FROM login_attempts WHERE username = ? AND attempt_time > ?",
        (username, ten_minutes_ago)
    )
    fail_count = cursor.fetchone()['fail_count']

    if fail_count >= 5:
        conn.close()
        return jsonify({'msg': '登入失敗次數過多', 'show_forget': True}), 400

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({'msg': '帳號尚未註冊'}), 400

    if user['password'] != password:
        cursor.execute(
            "INSERT INTO login_attempts (username, attempt_time) VALUES (?, ?)", 
            (username, datetime.now())
        )
        conn.commit()
        conn.close()
        return jsonify({'msg': '密碼錯誤'}), 400

    # 登入成功 → 清除錯誤紀錄
    cursor.execute("DELETE FROM login_attempts WHERE username = ?", (username,))
    conn.commit()
    conn.close()

    session['user'] = username
    return jsonify({"msg": "登入成功", "name": user['name']})

# ===================== 忘記密碼 API =====================
@app.route('/forget', methods=['POST'])
def forget():
    data = request.json
    username = data['username']
    name = data['name']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND name = ?", 
        (username, name)
    )
    user = cursor.fetchone()

    if user:
        cursor.execute("DELETE FROM login_attempts WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        return jsonify({'msg': f"您的密碼為：{user['password']}"})
    else:
        conn.close()
        return jsonify({'msg': "帳號或姓名不正確，無法找回密碼"}), 400

# ===================== 啟動 =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
