import sqlite3
import bcrypt

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL
        )
    ''')
    
    # 检查示例用户是否已存在，避免重复插入
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('testuser',))
    if cursor.fetchone()[0] == 0:
        # 对密码进行加密，并确保存储为字节类型
        hashed_password = bcrypt.hashpw('testpass'.encode('utf-8'), bcrypt.gensalt())
        cursor.execute('''
            INSERT INTO users (username, password) VALUES
            (?, ?)
        ''', ('testuser', hashed_password))
    
    conn.commit()
    conn.close()
