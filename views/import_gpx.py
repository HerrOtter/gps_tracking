import os
import sqlite3
import gpxpy
import datetime

def import_gpx():
    # Connect to SQLite database
    conn = sqlite3.connect('gps_tracking.db')
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS Person
                 (id INTEGER PRIMARY KEY,
                 name TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Fahrzeug
                 (id INTEGER PRIMARY KEY,
                 kennzeichen TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Tracks
                 (id INTEGER PRIMARY KEY,
                 name TEXT,
                 person_id INTEGER,
                 fahrzeug_id INTEGER,
                 datum date,
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
            filename_parts = filename.split("_")
            if len(filename_parts) >= 3:
                person_name = filename_parts[0]

            # Insert person data into Person table
            c.execute("INSERT INTO Person (name) VALUES (?)", (person_name,))
            person_id = c.lastrowid

            # Extract fahrzeug data
            fahrzeug_kennzeichen = filename_parts[1]

            # Insert fahrzeug data into Fahrzeug table
            c.execute("INSERT INTO Fahrzeug (kennzeichen) VALUES (?)", (fahrzeug_kennzeichen,))
            fahrzeug_id = c.lastrowid

            # Extract track data
            track_name = filename[:-4] # remove the '.gpx' extension from the filename

            # Insert track data into Tracks table
            c.execute("INSERT INTO Tracks (name, person_id, fahrzeug_id) VALUES (?, ?, ?)", (track_name, person_id, fahrzeug_id))
            track_id = c.lastrowid

            # Extract trackpoint data
            if gpx.tracks is not None:
                print("Track data found")
                if len(gpx.tracks) > 0:
                    for track in gpx.tracks:
                        if len(track.segments) > 0:
                            print("happy")
                            for segment in track.segments:
                                for point in segment.points:
                                    lat = point.latitude
                                    lon = point.longitude
                                    ele = point.elevation
                                    tp_time = point.time
                                    atemp = None
                                    hr = None
                                    if point.extensions is not None:
                                        for extension in point.extensions:
                                            if extension.tag.endswith("TrackPointExtension"):
                                                for child in extension.iter():
                                                    if child.tag.endswith("atemp"):
                                                        atemp = child.text
                                                    elif child.tag.endswith("hr"):
                                                        hr = child.text 
                                    c.execute("INSERT INTO Trackpoints (track_id, lat, lon, ele, time, atemp, hr) VALUES (?, ?, ?, ?, ?, ?, ?)", (track_id, lat, lon, ele, tp_time, atemp, hr))
                                    c.execute("UPDATE Tracks SET datum = ? WHERE id = ?", (tp_time, track_id))
                        else:
                            print("sad")
                            if gpx.waypoints is not None:
                                print("waypoints found")
                                print(gpx.waypoints)
                                for waypoint in gpx.waypoints:
                                    print("yippy")
                                    lat = waypoint.latitude
                                    lon = waypoint.longitude
                                    ele = waypoint.elevation
                                    tp_time = waypoint.time
                                    atemp = None
                                    hr = None
                                    if waypoint.extensions is not None:
                                        for extension in waypoint.extensions:
                                            if extension.tag.endswith("TrackPointExtension"):
                                                for child in extension.iter():
                                                    if child.tag.endswith("atemp"):
                                                        atemp = child.text
                                                    elif child.tag.endswith("hr"):
                                                        hr = child.text
                                    c.execute("INSERT INTO Trackpoints (track_id, lat, lon, ele, time, atemp, hr) VALUES (?, ?, ?, ?, ?, ?, ?)", (track_id, lat, lon, ele, tp_time, atemp, hr))
                                    c.execute("UPDATE Tracks SET datum = ? WHERE id = ?", (tp_time, track_id))
                else:
                    if gpx.waypoints is not None:
                        for waypoint in gpx.waypoints:
                            lat = waypoint.latitude
                            lon = waypoint.longitude
                            ele = waypoint.elevation
                            tp_time = waypoint.time
                            atemp = None
                            hr = None
                            if waypoint.extensions is not None:
                                for extension in waypoint.extensions:
                                    if extension.tag.endswith("TrackPointExtension"):
                                        for child in extension.iter():
                                            if child.tag.endswith("atemp"):
                                                atemp = child.text
                                            elif child.tag.endswith("hr"):
                                                hr = child.text
                            c.execute("INSERT INTO Trackpoints (track_id, lat, lon, ele, time, atemp, hr) VALUES (?, ?, ?, ?, ?, ?, ?)", (track_id, lat, lon, ele, tp_time, atemp, hr))
                            c.execute("UPDATE Tracks SET datum = ? WHERE id = ?", (tp_time, track_id))
            
            # Commit changes and log success
            conn.commit()
            log_file.write(f"{filename} successfully imported at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            print(f"{filename} successfully imported")

    # Close connection and log file
    conn.close()
    log_file.close()

    return "GPX files imported successfully."