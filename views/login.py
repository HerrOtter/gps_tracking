from flask import render_template, request
import sqlite3, bcrypt
from . import login_bp

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect("user.db")
        c = conn.cursor()

        query   = '''SELECT * FROM users WHERE username = ? AND password = ?'''
        c.execute(query, (username, password))
        user = c.fetchone()
        print(user)

        if user:
            session['user_id'] = user['id']
            print(session['user_id'])
            return render_template('map.html')
        else:
            return 'Login Failed'

    return render_template('login.html')