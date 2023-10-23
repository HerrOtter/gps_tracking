from flask import render_template, request
import sqlite3
from . import tracking_bp

@tracking_bp.route('/eingabe', methods=['GET', 'POST'])
def tracking():
    if request.method == 'POST':
        # Get form data from request
        name        = request.form['nick']
        kennzeichen = request.form['kfz']
        #datefrom    = request.form['datefrom']
        #dateto      = request.form['dateto']
        
        # Connect to database and execute query
        conn    = sqlite3.connect('gps_tracking.db')
        c       = conn.cursor()
        query   = '''SELECT tp.lat, tp.lon, tp.ele FROM person AS p
                        INNER JOIN Tracks AS t ON t.person_id = p.id
                        INNER JOIN Fahrzeug AS f on f.id = t.fahrzeug_id
                        INNER JOIN Trackpoints AS tp ON tp.track_id = t.id
                        WHERE p.name = ? AND f.kennzeichen = ?'''
        c.execute(query, (name, kennzeichen))
        trackpoints = c.fetchall()
        print(trackpoints)
        conn.close()

        # Convert trackpoints to coordinates list and render template
        coordinates = [(track[0], track[1]) for track in trackpoints]
        print(coordinates)
        return render_template('index.html', coordinates=coordinates)
