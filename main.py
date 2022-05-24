from flask import Flask, render_template, redirect, session, url_for, request, flash, g
import os
import sqlite3
# from FDataBase import FDataBase

# Конфигурация
DATABASE = 'flasksite.db'
DEBUG = True
SECRET_KEY = 'askl;vsjf;ldkmvskmdfms,m'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flasksite.db'))) # Переопределение пути к БД

menu = [
    {'name': 'Главная страница', 'url': 'index'},
    {'name': 'Вход', 'url': 'sign-in'},
    {'name': 'Регистрация', 'url': 'sign-up'}
]


def connect_db():
    """ Подключение к БД """
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row           # Превращаем кортежи в списки
    return conn


def create_db():
    """ Функция для создания таблиц БД """
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as file:
        db.cursor().executescript(file.read())
    db.commit()
    db.close()


def get_db():
    """ Соединиение БД и запросы """
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# dbase = None
# @app.before_request
# def before_request():
#     global dbase
#     db = get_db()
#     dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', menu=menu)


@app.route('/sign-in', methods=["POST", "GET"])
def sign_in():
    if 'userLogged' in session:
        flash('Вы уже авторизованы.')
        return redirect(url_for('index'))
    elif request.method == "POST" and request.form['username'] == 'selfedu' and request.form['password'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('index'))

    return render_template('signin.html', menu=menu)


@app.route('/sign-up', methods=["POST", "GET"]) # Обработчик страницы регистрации
def sign_up():
    if request.method == "POST":
        if request.form['password1'] == request.form['password2'] and '@' in request.form['email']:
            flash("Региcnрация успешна!")
        else:
            flash('Ошибка регистрации...')

    return render_template('signup.html', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)