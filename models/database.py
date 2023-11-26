import sqlite3
import os
import gpxpy

def create_tracking_tables():    
    conn = sqlite3.connect('gps_tracking.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS person
                (id             INTEGER PRIMARY KEY,
                initials        VARCHAR(2))''')

    c.execute('''CREATE TABLE IF NOT EXISTS vehicle
                (id             INTEGER PRIMARY KEY,
                license_plate   VARCHAR(10))''')

    c.execute('''CREATE TABLE IF NOT EXISTS track
                (id             INTEGER PRIMARY KEY,
                filename        VARCHAR(255),
                person_id       INTEGER,
                vehicle_id      INTEGER,
                date            VARCHAR(10),
                FOREIGN KEY (person_id)    REFERENCES person(id),
                FOREIGN KEY (vehicle_id)   REFERENCES vehicle(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS trackpoint
                (id             INTEGER PRIMARY KEY,
                track_id        INTEGER,
                latitude        REAL,
                longitude       REAL,
                elevation       REAL,
                date            VARCHAR(10),
                time            VARCHAR(8),
                temperature     REAL,
                hr              INTEGER,
                FOREIGN KEY (track_id) REFERENCES track(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS protocol
                (id             INTEGER PRIMARY KEY,
                filename        VARCHAR(255),
                track_id        INTEGER,
                is_valid        BOOLEAN,
                FOREIGN KEY (track_id) REFERENCES track(id))''')
    
    conn.close()

def create_user_table():
    conn = sqlite3.connect("user.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id             INTEGER PRIMARY KEY,
                username        VARCHAR(64) UNIQUE,
                password        VARCHAR(255))''')

    c.execute('''CREATE TABLE IF NOT EXISTS data
                (id             INTEGER PRIMARY KEY,
                initials        VARCHAR(2),
                forname         VARCHAR(64),
                surname         VARCHAR(64),
                FOREIGN KEY (id) REFERENCES users(id))''')
    

def test_tracking_tables():
    conn = sqlite3.connect('gps_tracking.db')
    c = conn.cursor()
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    
    assert ('person',) in tables
    assert ('vehicle',) in tables
    assert ('track',) in tables
    assert ('trackpoint',) in tables
    assert ('protocol',) in tables
    
    print("All tables were created successfully.")
    conn.close()
    return True

def test_user_table():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    
    assert ('users',) in tables
    assert ('data',) in tables
    
    print("All tables were created successfully.")
    conn.close()
    return True