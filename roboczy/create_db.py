from sqlite3 import *
conn = connect('db.db')
c = conn.cursor()
c.execute("CREATE TABLE users(username TEXT PRIMARY KEY, password TEXT, salt TEXT)")
c.execute("CREATE TABLE sessions(username TEXT, session_id TEXT, browser_id TEXT)")
c.execute("CREATE TABLE files(fid INTEGER PRIMARY KEY, filename TEXT, username TEXT, data BLOB)")
c.execute("CREATE TABLE snippets(sid INTEGER PRIMARY KEY, username TEXT, name TEXT, data TEXT)")
conn.commit()
conn.close()
