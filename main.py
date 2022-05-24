from flask import Flask, render_template, redirect, session, url_for, request, flash, g
import os
import sqlite3
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user
from UserLogin import UserLogin

# Конфигурация
DATABASE = 'flasksite.db'
DEBUG = True
SECRET_KEY = 'askl;vsjf;ldkmvskmdfms,m'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flasksite.db')))  # Переопределение пути к БД

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


# Список, на основании которого формируется шапка сайта
menu = [
    {'name': 'Главная страница', 'url': 'index'},
    {'name': 'Вход', 'url': 'sign-in'},
    {'name': 'Регистрация', 'url': 'sign-up'}
]

dbase = None


def connect_db():
    """ Подключение к БД """
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  # Превращаем кортежи в списки
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


@app.before_request  # Вспомогательная функция, которая подключает БД до запроса
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext  # Разрыв соединения с базой данных
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')  # Обработчик главной страницы
@app.route('/index', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if len(request.form['name']) > 3 and len(request.form['lastname']) > 3:
            response = dbase.addInput(request.form['name'], request.form['lastname'])
            flash('Данные записаны', 'success')
        else:
            flash('Ошибка', 'error')

    return render_template('index.html', menu=menu)


@app.route('/sign-in', methods=["POST", "GET"])  # Обработчик страницы авторизации
def sign_in():
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect('index')

        flash('Неверный логин или пароль.', 'error')

    return render_template('signin.html', menu=menu)


@app.route('/sign-up', methods=["POST", "GET"])  # Обработчик страницы регистрации
def sign_up():
    if request.method == "POST":
        if request.form['password1'] == request.form['password2'] and '@' in request.form['email'] \
                and len(request.form['username']) > 4 and len(request.form['password1']) > 4:  # Различные проверки
            hpsw = generate_password_hash(request.form['password1'])  # Создание хэш-пароля на основании введёного
            response = dbase.addUser(request.form['email'], request.form['username'], hpsw)  # Запись данных в БД
            flash("Региcnрация успешна!", category='success')
            return redirect('sign-in')
        else:
            flash('Ошибка регистрации...', category='error')

    return render_template('signup.html', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
