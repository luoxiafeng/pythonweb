from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import bcrypt
from create_db import create_database  # 导入创建数据库的函数

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于闪存消息

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')

    # 数据库验证
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    # 直接使用数据库中的字节形式的密码，不进行编码转换
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return redirect(url_for('success'))  # 登录成功跳转页面
    else:
        flash('此用户不存在或密码错误')  # 显示错误信息
        return redirect(url_for('login'))  # 返回登录页面

@app.route('/success')
def success():
    return 'Login Successful! Welcome to the next page.'

if __name__ == '__main__':
    create_database()  # 在应用启动时调用创建数据库的函数
    app.run(debug=True)
