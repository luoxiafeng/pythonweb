import sqlite3

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # 检查示例用户是否已存在，避免重复插入
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('testuser',))
    if cursor.fetchone()[0] == 0:
        # 直接使用明文密码，不进行加密
        plain_password = 'testpass'
        cursor.execute('''
            INSERT INTO users (username, password) VALUES
            (?, ?)
        ''', ('testuser', plain_password))
    
    conn.commit()
    conn.close()
