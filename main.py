
from flask import Flask, render_template, request
from flask_leaflet import Leaflet, Map, Marker 
import sqlite3

app = Flask(__name__)

@app.route('/eingabe', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nick = request.form['nick']
        kfz = request.form['kfz']
        datefrom = request.form['datefrom']
        dateto = request.form['dateto']
        print(nick, kfz, datefrom, dateto)
        conn = sqlite3.connect('gps_tracking.db')
        c = conn.cursor()
        query = "SELECT * FROM tracks WHERE nick=? OR kfz=? OR date BETWEEN ? AND ?"
        c.execute(query, (nick, kfz, datefrom, dateto))
        tracks = c.fetchall()
        conn.close()
        markers = [Marker(location=[track[1], track[2]]) for track in tracks]
        return render_template('index.html', map=Map(center=[51.505, -0.09], zoom=13, markers=markers))
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
