# app.py
from flask import Flask, render_template
from views.tracking import tracking_bp
from views.import_gpx import import_gpx

app = Flask(__name__)

# Register the tracking blueprint
app.register_blueprint(tracking_bp)

@app.route('/')
def home():
    import_gpx()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
