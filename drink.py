# -*- coding: utf-8 -*-
from vial import Vial, render_template
from sqlite3 import *
#import sqlite3
import crypt
import uuid

def index(headers, body, data):
    message = 'jestes nie zalogowany'
    if 'cookie' in headers and headers['cookie'] is not None:
        cookies = headers['cookie']
        cookies_list = cookies.split('; ')
        cookie_dict = {}
        for cookie in cookies_list:
            cookie = cookie.split('=')
            cookie_dict[cookie[0]] = cookie[1]
        if 'cookie_session' in cookie_dict:
            cookie_id = cookie_dict['cookie_session']
            conn = connect('database_for_login.db')
            c = conn.cursor()
            c.execute('SELECT cookie, login FROM cookies WHERE cookie = ?;', (cookie_id,) )
            res = c.fetchall()
            conn.close()
            if res:
                message = 'jestes zalogowany'
                return render_template('index.html', message=message), 200, {}
    return render_template('index.html', message=message), 200, {}


def login(headers, body, data):
    if 'cookie' in headers and headers['cookie'] is not None:
        cookies = headers['cookie']
        cookies_list = cookies.split('; ')
        cookie_dict = {}
        for cookie in cookies_list:
            cookie = cookie.split('=')
            cookie_dict[cookie[0]] = cookie[1]
        print cookie_dict
        if 'cookie_session' in cookie_dict:
            cookie_id = cookie_dict['cookie_session']
            conn = connect('database_for_login.db')
            c = conn.cursor()
            c.execute('SELECT * FROM cookies WHERE cookie = ?;', (cookie_id,) )
            res = c.fetchall()
            conn.close()
            if res:
                return '', 307, {'Location': '/index'}
    # ^^^ sprawdza czy zalogowany i przekierowywuje
    if 'login' in data and 'password' in data:
        login = str(data['login'])
        password = str(data['password'])
        conn = connect('database_for_login.db')
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE login = ?;', (login,))
        res = c.fetchall()
        if len(res) > 0:
            password_from_db = res[0][0]
            salt = password_from_db[:2]
            if password_from_db == crypt.crypt(password, salt):
                c.execute('DELETE FROM cookies WHERE login = ?;', (login,))
                conn.commit()
                cookie_id = str(uuid.uuid4())
                c.execute('INSERT INTO cookies (cookie, login) VALUES (?, ?);', (cookie_id, login))
                conn.commit()
                conn.close()
                return '', 307, {'Set-Cookie': 'cookie_session={}'.format(cookie_id), 'Location': '/index'}
            #return # bledne haslo
        #return # bledne login
        conn.close()
        message = 'bledny login lub haslo'
        return render_template('login.html', message=message), 200, {}
        
    html = render_template('login.html')
    return html, 200, {}

def register(headers, body, data):
    #Musi być łączenie z bazą danych,
    print 'data', data #Najpierw CO drukuję, a potem jeszcze zawartość tego!
    print 'body', body
    if ('login_register' in data) and ('password_register' in data):
        usr = str(data['login_register'])
        pw = str(data['password_register'])
        print usr
        print pw


        conn = connect('db.db')
        c = conn.cursor()
        k = c.execute("SELECT username FROM users WHERE username=?", (usr,))
        username = k.fetchone()

        conn.commit()
        conn.close()
        tmp=0
        message = 'Dane ok'

    else:
        tmp=1
        message = u'Nie podano wystarczająco dużo danych'

    html = render_template('register_form.html', message=message, tmp=tmp)
    return html, 200, {}

routes = {
    '/': index,
    '/index': index,
    '/login': login,
}

app = Vial(routes, prefix='/bach/drink', static='/static').wsgi_app()
