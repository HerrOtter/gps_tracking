# from flask import render_template, request
# import sqlite3
# from . import register_bp

# @register_bp.app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         add_user(username, password)

#         return redirect(url_for('login'))

#     return render_template('register.html')