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
            c.execute('SELECT cookie, login FROM cookies WHERE cookie = ?;', (cookie_id,) )
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
                return 'whatever', 307, {'Set-Cookie': 'cookie_session={}'.format(cookie_id), 'Location': '/index'}
            #return # bledne haslo
        #return # bledne login
        
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

    # Spr. czy usr juz istnieje i dopiero przypis z db
    html = render_template('register_form.html', message=message, tmp=tmp)
    return html, 200, {}

#    body_dict = urlparse.parse_qs(body) #W jakim zakresie jest to pobierane?
#    print type(body_dict[]) body to jest po prostu query string i z tego trzeba by zrobić słownik!
#Zwrócenie do zinterp. przez przeg.

""" k = c.execute("SELECT username FROM users WHERE username=?", (usr,))
    username = k.fetchone()

    # Jak szukałem różnych funkcji, to na takie coś natrafiłem
    hashlib.sha256(password).hexdigest() #Odpowiednie zahaszhowanie hasła i w ogóle.
    q = cur.execute("SELECT id,username,password,salt FROM users WHERE username=?", (usr,)) #Wczytywanie loginu
    cookie = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32)) #Sól
    cur_s.execute('INSERT OR REPLACE INTO sessions VALUES(?, ?, ?, ?)', (db_id, usr, cookie, browser_id)) #Umieszczanie danych do sesji
"""
"""def register(headers, body, data):
    conn = connect('db.db')
    c = conn.cursor()
#    db = connect('users.db')
#    cur = db.cursor()
    usr = str(data['username'])
    passw = str(data['password'])
    q = c.execute("SELECT username FROM users WHERE username=?", (usr,))
    username = q.fetchone()
    if username is not None and username[0] == usr:
        db.commit()
        db.close()
        return render_template("message.html",
                               msg=esc("User: '" + usr + "' already exists!"),
                               redirect_url="https://od.iem.pw.edu.pl:5443/signup",
                               url_name=esc("Back to sign up page")), 409, {}

    salt = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(12))
    hashed_pass = hashlib.sha256(passw + salt).hexdigest()
    cur.execute("INSERT INTO users (username, password, salt) VALUES(?, ?, ?)", (usr, hashed_pass, salt))
    db.commit()
    db.close()

    return render_template("message.html",
                           msg=esc("Successfully registered!"),
                           redirect_url="https://od.iem.pw.edu.pl:5443/welcome",
                           url_name=esc("Go to sign in page")), 200, {}
"""

def signin(headers, body, data):
    html3 = render_template('signin_form.html')
    return html3, 200, {}

#def index(headers, body, data):
#    return 'Hello', 200, {} #zwracane są tak naprawdę krotki!

def hello(headers, body, data, name):
    return 'Howdy ' + name, 200, {}

def upload(headers, body, data):
    my_list = range(1, 11)
    html = render_template('upload.html', body="cialo", data=data, my_list=my_list)
    return html, 200, {}
# Odpowiedzialna jest za zwracanie html-a. Definiuje w upload.html wszystkie pętle, for-y, if-y. Wrzucam tego uploada (nazwa i zmienne)
# To, co po lewej, to MUSI być w uload.html w srodku
# Ekzekwuje odpowiednio kod html-a.
# Przetwarza wstawiając odpowiednie argumenty i zwraca kod HTML-owy, który przetworzy jinja2 w podany przez nas sposób!

routes = {
    '/': index,
    '/index': index,
    '/hello/{name}': hello,
    '/upload': upload,
    '/register': register,
    '/login': login,
    #Wchodząc na odpowiednią stronę wywołuje odpowiednią metodę!
}

app = Vial(routes, prefix='/bach/drink', static='/static').wsgi_app()
#Te zmienne teoretycznie NIE musiałyby być przypisane (prefix, static, natomiast routes już TAK, bo nie była zainicjalizowana w pliku
#źródłowym, ale te inicjalizacje tutaj były zrobione na potrzeby innego projektu i NIE są ważne!
#To po prostu odpowiednio inicjalizuje ten tzw. "konstruktor" klasy, natomiast wywoływana jest po prostu metoda już bez podawania jakich-
#kolwiek argumentów!

#Po co on tu przekazuje 'prefix' i 'static', skoro potem je i tak przyrównuje do pustego?

