from flask import render_template, request
import sqlite3
from . import tracking_bp

@tracking_bp.route('/eingabe', methods=['GET', 'POST'])
def tracking():
    if request.method == 'POST':

        initials        = request.form['nick']
        license_plate = request.form['kfz']
        datefrom    = request.form['datefrom']
        dateto      = request.form['dateto']

        if datefrom == '' and dateto == '':
            datefrom = '1900-01-01'
            dateto = '2100-01-01'
        
        print(initials, license_plate, datefrom, dateto)
        
        conn    = sqlite3.connect('gps_tracking.db')
        c       = conn.cursor()
        query   = '''SELECT tp.latitude, tp.longitude, tp.elevation FROM person AS p
                        INNER JOIN track        AS t    ON t.person_id  = p.id
                        INNER JOIN vehicle      AS v    ON v.id         = t.vehicle_id
                        INNER JOIN trackpoint   AS tp   ON tp.track_id  = t.id
                        WHERE p.initials = ? AND v.license_plate = ? AND (SELECT is_valid FROM protocol WHERE is_valid = '1') AND t.date BETWEEN ? AND ?'''
        c.execute(query, (initials, license_plate, datefrom, dateto))
        trackpoints = c.fetchall()
        for trackpoint in trackpoints:
            print(trackpoint)
        conn.close()

        coordinates = [(track[0], track[1]) for track in trackpoints]
        return render_template('index.html', coordinates=coordinates)
