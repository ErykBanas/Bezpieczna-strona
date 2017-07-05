# -*- coding: utf-8 -*-
from vial import Vial, render_template
from sqlite3 import *
import urlparse

#Spr., czy coś zostało przesłane - dodać.
def register(headers, body, data):
    #Musi być łączenie z bazą danych,
    print 'data', data #Najpierw CO drukuję, a potem jeszcze zawartość tego!
    html = render_template('register_form.html')
    print "type(data['login_register'])", type(data['login_register'])
#    body_dict = urlparse.parse_qs(body) #W jakim zakresie jest to pobierane?
#    print type(body_dict[])

    conn = connect('db.db')
    c = conn.cursor()
    usr = str(data['login_register'])
#    passw = str(data['password_register'])
#    print usr
#    print passw
    return html, 200, {}

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

def index(headers, body, data):
    return 'Hello', 200, {} #zwracane są tak naprawdę krotki!

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
    #Wchodząc na odpowiednią stronę wywołuje odpowiednią metodę!
}

app = Vial(routes, prefix='/bach/drink', static='/static').wsgi_app()
#Te zmienne teoretycznie NIE musiałyby być przypisane (prefix, static, natomiast routes już TAK, bo nie była zainicjalizowana w pliku
#źródłowym, ale te inicjalizacje tutaj były zrobione na potrzeby innego projektu i NIE są ważne!
#To po prostu odpowiednio inicjalizuje ten tzw. "konstruktor" klasy, natomiast wywoływana jest po prostu metoda już bez podawania jakich-
#kolwiek argumentów!

#Po co on tu przekazuje 'prefix' i 'static', skoro potem je i tak przyrównuje do pustego?

