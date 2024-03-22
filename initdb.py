import sqlite3
import os

def setup():

    os.remove("database.db")


    con = sqlite3.connect('database.db')
    with open('database.sql') as f:
        con.executescript(f.read())
    con.commit()
    con.close()