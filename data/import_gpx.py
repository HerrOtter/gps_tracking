import os
import sqlite3
import gpxpy
import time
import datetime

# Connect to SQLite database
conn = sqlite3.connect('gps_tracking.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS Person
             (id INTEGER PRIMARY KEY,
             name TEXT,
             email TEXT,
             phone TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Fahrzeug
             (id INTEGER PRIMARY KEY,
             marke TEXT,
             modell TEXT,
             kennzeichen TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Tracks
             (id INTEGER PRIMARY KEY,
             name TEXT,
             person_id INTEGER,
             fahrzeug_id INTEGER,
             FOREIGN KEY (person_id) REFERENCES Person(id),
             FOREIGN KEY (fahrzeug_id) REFERENCES Fahrzeug(id))''')

c.execute('''CREATE TABLE IF NOT EXISTS Trackpoints
             (id INTEGER PRIMARY KEY,
             track_id INTEGER,
             lat REAL,
             lon REAL,
             ele REAL,
             time TEXT,
             atemp REAL,
             hr INTEGER,
             FOREIGN KEY (track_id) REFERENCES Tracks(id))''')

# Create log file
log_file = open("import_log.txt", "a")

for filename in os.listdir('./data/gpx'):
    if filename.endswith('.gpx'):
        # Parse GPX file
        with open(os.path.join('./data/gpx', filename), 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)

        # Extract person data
        person_name = gpx.author_name
        person_email = gpx.author_email
        person_phone = gpx.author_link

        # Insert person data into Person table
        c.execute("INSERT INTO Person (name, email, phone) VALUES (?, ?, ?)", (person_name, person_email, person_phone))
        person_id = c.lastrowid

        # Extract fahrzeug data
        fahrzeug_marke = gpx.name
        fahrzeug_modell = gpx.description
        fahrzeug_kennzeichen = gpx.author_link

        # Insert fahrzeug data into Fahrzeug table
        c.execute("INSERT INTO Fahrzeug (marke, modell, kennzeichen) VALUES (?, ?, ?)", (fahrzeug_marke, fahrzeug_modell, fahrzeug_kennzeichen))
        fahrzeug_id = c.lastrowid

        # Extract track data
        track_name = filename[:-4] # remove the '.gpx' extension from the filename

        # Insert track data into Tracks table
        c.execute("INSERT INTO Tracks (name, person_id, fahrzeug_id) VALUES (?, ?, ?)", (track_name, person_id, fahrzeug_id))
        track_id = c.lastrowid

        # Extract trackpoint data
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat = point.latitude
                    lon = point.longitude
                    ele = point.elevation
                    time = point.time
                    atemp = None
                    hr = None
                    if point.extensions is not None:
                        for extension in point.extensions:
                            if extension.tag.endswith("TrackPointExtension"):
                                for child in extension.getchildren():
                                    if child.tag.endswith("atemp"):
                                        atemp = child.text
                                    elif child.tag.endswith("hr"):
                                        hr = child.text

                    # Insert trackpoint data into Trackpoints table
                    c.execute("INSERT INTO Trackpoints (track_id, lat, lon, ele, time, atemp, hr) VALUES (?, ?, ?, ?, ?, ?, ?)", (track_id, lat, lon, ele, time, atemp, hr))

        # Commit changes and log success
        conn.commit()
        log_file.write(f"{filename} successfully imported at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"{filename} successfully imported")

# Close connection and log file
conn.close()
log_file.close()
