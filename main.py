from flask import Flask, render_template, redirect, session, url_for, request

app = Flask(__name__)
menu = [
    {'name': 'Главная страница', 'url': ''},
    {'name': 'Вход', 'url': 'sign-in'},
    {'name': 'Регистрация', 'url': 'sign-up'}
]


@app.route('/')
def index():
    return render_template('index.html', menu=menu)


@app.route('/sign-in', methods=["POST"])
def sign_in():
    # if 'userLogged' in session:
    #     return redirect(url_for('profile', username=session['userLogged']))
    # elif request.form['name'] == 'selfedu' and request.form['password' == '123']:
    #     session['userLogged'] = request.form['name']
    #     return redirect(url_for('profile', username=session['userLogged']))

    return render_template('signin.html', menu=menu)


@app.route('/sign-up', methods=["POST"])
def sign_up():
    return render_template('signup.html', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
