from flask import Flask, url_for, render_template, redirect
from data import db_session
import forms
app = Flask(__name__)

# S - safety
app.config['SECRET_KEY'] = 'SECRET_KEY'


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        form.login_user()
        return redirect('/')
    return render_template('login.jinja', title='Login', form=form)


@app.route('/user/<user_login>')
def user_page(user_login):
    return render_template('user_page.jinja', title='Main Page')


@app.route('/messanger')
def messanger():
    return render_template('messanger.jinja', title='Messanger')


@app.route('/')
def index():
    return render_template('index.jinja', title='Main Page')


def main():
    db_session.global_init('db/db.db')
    app.run(port=8080, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()
