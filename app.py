from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from functools import wraps
from create_db import create_database  # 导入创建数据库的函数

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于闪存消息

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('请先登录以访问该页面。')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/order_form')
@login_required
def order_form():
    return render_template('order_form.html')  # 渲染订单页面


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')

    # 检查用户名和密码是否为空
    if not username or not password:
        flash('请输入用户名和密码')
        return redirect(url_for('login'))  # 返回登录页面

    # 数据库验证
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    # 直接比较密码字符串，不进行加密
    if user and password == user['password']:
        session['logged_in'] = True
        session['username'] = username
        flash('登录成功！')
        return redirect(url_for('dashboard'))  # 确保登录后跳转到控制台页面
    else:
        flash('此用户不存在或密码错误')  # 显示错误信息
        return redirect(url_for('login'))  # 返回登录页面

@app.route('/logout')
def logout():
    session.clear()  # 清除会话
    flash('您已成功注销。')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    username = session.get('username', '用户')  # 获取当前登录的用户名
    return render_template('dashboard.html', username=username)  # 渲染控制台页面并传递用户名

@app.route('/help_center')
@login_required
def help_center():
    username = session.get('username', '用户')  # 获取当前登录的用户名
    return render_template('help_center.html', username=username)  # 渲染帮助中心页面并传递用户名

# 定义购买打卡服务的路由
@app.route('/purchase/<app_name>')
def purchase(app_name):
    # 根据不同的 app_name 显示相应的页面或处理逻辑
    return f"购买打卡服务 - {app_name}"

if __name__ == '__main__':
    create_database()  # 在应用启动时调用创建数据库的函数
    app.run(debug=True)
