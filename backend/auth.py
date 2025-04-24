from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import jwt
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = 'your-secret-key'  # In production, use environment variable

def init_db():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sales_employees
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not all(k in data for k in ('username', 'password', 'email')):
        return jsonify({'message': 'Missing required fields'}), 400
    
    hashed_password = generate_password_hash(data['password'])
    
    try:
        conn = sqlite3.connect('sales.db')
        c = conn.cursor()
        c.execute('INSERT INTO sales_employees (username, password, email) VALUES (?, ?, ?)',
                 (data['username'], hashed_password, data['email']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username or email already exists'}), 409
    except Exception as e:
        return jsonify({'message': 'Error creating user'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in ('username', 'password')):
        return jsonify({'message': 'Missing username or password'}), 400
    
    try:
        conn = sqlite3.connect('sales.db')
        c = conn.cursor()
        c.execute('SELECT * FROM sales_employees WHERE username = ?', (data['username'],))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], data['password']):
            token = jwt.encode({
                'user_id': user[0],
                'username': user[1],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, SECRET_KEY)
            return jsonify({
                'token': token,
                'username': user[1]
            }), 200
        return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'message': 'Error during login'}), 500

# Initialize the database when the module is imported
init_db()
