from flask import render_template, request, redirect, url_for
import sqlite3, bcrypt
from . import register_bp

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        forname = request.form['forname']
        surname = request.form['surname']
        password = request.form['password']

        # Hash das Passwort
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect("user.db")
        c = conn.cursor()

        query   = '''INSERT INTO users (username, password) VALUES (?, ?)'''
        c.execute(query, (username, hashed_password))
        user_id = c.lastrowid

        initials = forname[0] + surname[0]
        query   = '''INSERT INTO data (initials, forname, surname) VALUES (?, ?, ?)'''
        c.execute(query, (initials, forname, surname))

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template('register.html')