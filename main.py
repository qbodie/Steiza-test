import sqlite3

from flask import Flask, render_template, redirect, request, flash, g
from flask_login import LoginManager, login_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from FDataBase import FDataBase
from UserLogin import UserLogin

# Конфигурация
DEBUG = True
SECRET_KEY = 'askl;vsjf;ldkmvskmdfms,m'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasksite.db'

db = SQLAlchemy(app)

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


class Contacts(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=True)


class Inputs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    lastname = db.Column(db.String(50))


dbase = None


def connect_db():
    """ Подключение к БД """
    conn = sqlite3.connect('flasksite.db')
    conn.row_factory = sqlite3.Row  # Превращаем кортежи в списки
    return conn


def get_db():
    """ Соединиение БД и запросы """
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request  # Вспомогательная функция, которая подключает БД до запроса
def before_request():
    global dbase
    d_b = get_db()
    dbase = FDataBase(d_b)


@app.teardown_appcontext  # Разрыв соединения с базой данных
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')  # Обработчик главной страницы
@app.route('/index', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        if len(name) > 3 and len(lastname) > 3:
            user = Inputs(name=name, lastname=lastname)
            db.session.add(user)
            db.session.commit()
            flash('Данные записаны', 'success')
        else:
            flash('Ошибка', 'error')

    return render_template('index.html', menu=menu, title="Главная страница")


@app.route('/sign-in', methods=["POST", "GET"])  # Обработчик страницы авторизации
def sign_in():
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect('index')

        flash('Неверный логин или пароль.', 'error')

    return render_template('signin.html', menu=menu, tetle='Вход')


@app.route('/sign-up', methods=["POST", "GET"])  # Обработчик страницы регистрации
def sign_up():
    if request.method == "POST":
        if request.form['password1'] == request.form['password2'] and '@' in request.form['email'] \
                and len(request.form['username']) > 4 and len(request.form['password1']) > 4:  # Различные проверки
            hpsw = generate_password_hash(request.form['password1'])  # Создание хэш-пароля на основании введёного
            response = dbase.addUser(request.form['username'], request.form['email'], hpsw)  # Запись данных в БД
            if response:
                flash("Региcтрация успешна!", category='success')
                return redirect('sign-in')
            return redirect('sign-up')
        else:
            flash('Ошибка регистрации...', category='error')

    return render_template('signup.html', menu=menu, title='Регистрация')


if __name__ == '__main__':
    app.run(debug=True)
