import sqlite3

DB='vuln_task1.db'

def init():
    c=sqlite3.connect(DB)
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute("INSERT OR IGNORE INTO users(username,password) VALUES('alice','alicepass')")
    c.commit(); c.close()

def login(username,password):
    c=sqlite3.connect(DB)
    q="SELECT id FROM users WHERE username='%s' AND password='%s'"%(username,password)
    row=c.execute(q).fetchone(); c.close(); return row is not None
