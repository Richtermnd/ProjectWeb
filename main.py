from flask import Flask, url_for, render_template, redirect
from flask_login import login_required, current_user, login_user, logout_user, LoginManager

from data import db_session
from data import models
import forms
from forms.form_exeptions import *
app = Flask(__name__)

# S - safety
app.config['SECRET_KEY'] = 'SECRET_KEY'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(models.User, user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/sign_in')


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    form = forms.SignInForm()
    if form.validate_on_submit():
        try:
            login_user(**form.get_user())
            return redirect(f'/user/{current_user.login}')
        except UserNotExistException:
            error = 'User with this email does not exist'
        except WrongPasswordException:
            error = 'Wrong Password'
        return render_template('sign_in.jinja', form=form, error=error)
    return render_template('sign_in.jinja', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        form.login_user()
        return redirect('/')
    return render_template('login.jinja', title='Login', form=form)


@app.route('/user/<user_login>')
@login_required
def user_page(user_login):
    return render_template('user_page.jinja', title='User Page', user=current_user)


@app.route('/messanger')
@login_required
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
