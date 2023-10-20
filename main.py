
from flask import Flask, render_template, request
from flask_leaflet import Leaflet, Map, Marker 
import sqlite3

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html', markers=[])


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
        query = '''SELECT tp.lat, tp.lon, tp.ele FROM person AS p
                    INNER JOIN Tracks AS t ON t.person_id = p.id
                    INNER JOIN Fahrzeug AS f on f.id = t.fahrzeug_id
                    INNER JOIN Trackpoints AS tp ON tp.track_id = t.id
                    WHERE p.name = ? AND f.kennzeichen = ?'''
        if datefrom == '':
            datefrom = '0000-00-00'
        if dateto == '':
            dateto = '9999-99-99'
        c.execute(query, (nick, kfz))
        trackpoints = c.fetchall()
        conn.close()
    
        # Erstelle eine Liste von Markern aus den Trackpunkten
        markers = [{'lat': track[0], 'lng': track[1]} for track in trackpoints]
        print(markers)
    
        return render_template('index.html', markers=markers)
        
        
#         conn = sqlite3.connect('gps_tracking.db')
#         c = conn.cursor()
#         query = '''SELECT tp.lat, tp.lon, tp.ele FROM person AS p
#                     INNER JOIN Tracks AS t ON t.person_id = p.id
#                     INNER JOIN Fahrzeug AS f on f.id = t.fahrzeug_id
#                     INNER JOIN Trackpoints AS tp ON tp.track_id = t.id
#                     WHERE p.name = ? AND f.kennzeichen = ?'''
#         if datefrom == '':
#             datefrom = '0000-00-00'
#         if dateto == '':
#             dateto = '9999-99-99'
#         c.execute(query, (nick, kfz))
#         trackpoints = c.fetchall()
#         conn.close()
    
#         # Erstelle eine Liste von Markern aus den Trackpunkten
#         markers = [Marker(latlng=[track[0], track[1]]) for track in trackpoints]

#     # Rendere die Karte mit Leaflet und flask-leaflet
#     return render_template('index.html', map=Map('map', center=[51.505, -0.09], zoom=13, markers=markers))

if __name__ == '__main__':
    app.run(debug=True)
