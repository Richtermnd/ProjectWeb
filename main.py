# Flask imports
from flask import Flask, url_for, render_template, redirect, request, session
from flask_login import login_required, current_user, login_user, logout_user, LoginManager

# db imports
from data import db_session
from data import models

# forms imports
import forms
from forms.form_exeptions import *

from tools import *


# init app
app = Flask(__name__)


# -- config --
app.config['SECRET_KEY'] = 'SECRET_KEY'  # S - safety
login_manager = LoginManager()
login_manager.init_app(app)


# user session stuff

@login_manager.user_loader
def load_user(user_id):
    """ User session """
    with db_session.create_session() as ses:
        return ses.get(models.User, user_id)    


@app.route('/logout')
@login_required
def logout():
    """ Logout """
    logout_user()
    return redirect('/sign_in')


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    """ Sign in """
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
    """ Login """
    form = forms.LoginForm()
    if form.validate_on_submit():
        form.login_user()
        return redirect('/')
    return render_template('login.jinja', title='Login', form=form)


# user props

@app.route('/user/<user_login>')
@login_required
def user_page(user_login):
    """ Return User Page """
    with db_session.create_session() as ses:
        user = ses.get(models.User, user_login)
    return render_template('user_page.jinja', title='User Page', user=user)


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = forms.UserForm(**current_user.form_data())
    if form.validate_on_submit():
        form.confirm_changes(current_user)
        return redirect('/user/1')
    return render_template('account.jinja', form=form, user=current_user)


@app.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    form = forms.PostForm()
    if form.validate_on_submit():
        try:
            form.create_post()
        except FormFileException:
            error = 'File Error'
            return render_template('post_form.jinja', form=form, error=error)
        return redirect(f'/user/{current_user.login}')
    return render_template('post_form.jinja', form=form)


# messanger

@app.route('/messanger', methods=['POST', 'GET'])
@login_required
def messanger():
    chat_id = session.get('chat', None)  # get active chat from cookie
    form = forms.MessageForm()

    with db_session.create_session() as ses:
        chat = ses.get(models.Chat, chat_id)
        
        if form.validate_on_submit():
            form.create_message(current_user, chat)
            return redirect('/messanger')
        
        return render_template('messanger.jinja', 
                                title='Messanger', 
                                user=current_user, 
                                chat=chat,
                                form=form)


@app.route('/active_chat/<id>')
@login_required
def active_chat(id):
    """ Set active chat in cookie """
    session['chat'] = id
    return redirect('/messanger')


# other

@app.route('/')
def index():
    return render_template('index.jinja', title='Main Page')


@app.route('/load_file', methods=['POST', 'GET'])
@login_required
def test_load_file():
    """ 
    It's inly for test loading files 
    Don't forget remove this
    """
    if request.method == 'POST':
        file = request.files['file']
        create_file(file)
    return render_template('load_file.jinja')


def main():
    db_session.global_init('db/db.db')
    app.run(port=8080, host='localhost', debug=True)


if __name__ == '__main__':
        main()
