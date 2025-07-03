import sqlite3
from env import database_path

def create_db():
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS websites (name TEXT, url TEXT, owner TEXT, added TEXT)')
    con.commit()
    con.close()

def list_all_sites():
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.execute('SELECT name, url, owner, added FROM websites')
    return cur.fetchall()

def insert_site(name, url, owner, date):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    cur.executemany('INSERT INTO websites VALUES (?, ?, ?, ?)', [(name, url, owner, date)])
    con.commit()
    con.close()

def get_site_index(target_url, sites):
    normalized_url = target_url.strip().strip("/").lower()
    for i, (_, normalized_url, _, _) in enumerate(sites):
        if normalized_url == target_url:
            return i
        
    return None