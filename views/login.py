# from flask import render_template, request
# import sqlite3
# from . import login_bp

# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         user = query_db('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], one=True)

#         if user:
#             session['user_id'] = user['id']
#             return 'Logged in successfully!'
#         else:
#             return 'Login Failed'

#     return render_template('login.html')