# app.py
from flask import Flask, render_template
from views.tracking import tracking_bp
from views.register import register_bp
from views.login import login_bp
from models import function, database

app = Flask(__name__)

app.register_blueprint(tracking_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)

@app.route('/')
def home():
    database.create_tracking_tables()
    database.create_user_table()

    valid_tracking_tables = database.test_tracking_tables()
    valid_user_table = database.test_user_table()

    if not valid_tracking_tables == True or not valid_user_table == True:
        print("Tracking Tables: ", valid_tracking_tables)
        print("User Table: ", valid_user_table)
        print("The tables were not created successfully. Please check the database and try again.")
        exit()
    return render_template('login.html')

if __name__ == '__main__':       
    app.run(debug=True)

    
