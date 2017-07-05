# -*- coding: utf-8 -*-
import sqlite3

connection = sqlite3.connect('database_for_login.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE users (login TEXT PRIMARY KEY, password TEXT);')
cursor.execute('INSERT INTO users (login, password) VALUES ("lalala", "CYiPTFM.tzRwA");')
cursor.execute('CREATE TABLE cookies (cookie TEXT, login TEXT, FOREIGN KEY (login) REFERENCES users(login));')
connection.commit()
connection.close()

