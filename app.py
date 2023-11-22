# app.py
from flask import Flask, render_template
from views.tracking import tracking_bp
from models import function

app = Flask(__name__)

app.register_blueprint(tracking_bp)

@app.route('/')
def home():
    function.create_tracking_tables()
    tables_are_valid = function.test_created_tables()

    if not tables_are_valid:
        print("The tables were not created successfully. Please check the database and try again.")
        exit()
    else:
        function.import_gpx_files()
    return render_template('index.html')

if __name__ == '__main__':       
    app.run(debug=True)

    
