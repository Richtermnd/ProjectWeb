import random
import io

# Flask imports
from flask import Flask, url_for, render_template, redirect, request, session, send_file
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, AnonymousUserMixin
from flask_restful import Api

# db imports
from data import db_session
from data import models

# forms imports
import forms
from forms.form_exeptions import *

# other
from config import SECRET_KEY
from tools import *
import filters
import api


# init app
app = Flask(__name__)
api.init(Api(app))
filters.init(app)


# -- config --
app.config['SECRET_KEY'] = SECRET_KEY  # S - safety
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
            return redirect(f'/user/{current_user.id}')
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
        return redirect('/sign_in')
    return render_template('login.jinja', title='Login', form=form)


# user props

@app.route('/user/<user_id>')
@login_required
def user_page(user_id):
    """ Return User Page """
    session['last_page'] = f'/user/{user_id}'
    with db_session.create_session() as ses:
        user = ses.get(models.User, user_id)
        return render_template('user_page.jinja', title='User Page', user=user)


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = forms.UserForm(**current_user.form_data())
    if form.validate_on_submit():
        form.confirm_changes(current_user)
        return redirect(f'/user/{current_user.id}')
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
        return redirect(f'/user/{current_user.id}')
    return render_template('post_form.jinja', form=form)


# messanger

@app.route('/messanger', methods=['POST', 'GET'])
@login_required
def messanger():
    chat_id = session.get('chat', None)  # get active chat from cookie
    form = forms.MessageForm()
    with db_session.create_session() as ses:
        chat = ses.get(models.Chat, chat_id)
        user = ses.get(models.User, current_user.id)
        
        if form.validate_on_submit():
            form.create_message(current_user, chat)
            return redirect('/messanger')
        return render_template('messanger.jinja', 
                                title='Messanger', 
                                user=user, 
                                chat=chat,
                                form=form)


@app.route('/active_chat/<id>')
@login_required
def active_chat(id):
    """ Set active chat in cookie """
    session['chat'] = id
    return redirect('/messanger')


@app.route('/create_chat', methods=['POST', 'GET'])
def create_chat():
    form = forms.ChatForm()
    if form.validate_on_submit():
        form.create_chat()
        return redirect('/messanger')
    return render_template('chat_form.jinja', form=form)


@app.route('/chat/<chat_id>', methods=['POST', 'GET'])
def edit_chat(chat_id):
    with db_session.create_session() as ses:
        chat = ses.get(models.Chat, chat_id)
        form = forms.ChatForm(**chat.form_data())
        if form.validate_on_submit():
            form.update(chat)
            return redirect('\messanger')
        return render_template('chat_form.jinja', form=form)


@app.route('/delete_chat/<chat_id>')
def delete_chat(chat_id):
    with db_session.create_session() as ses:
        chat = ses.get(models.Chat, chat_id)
        ses.delete(chat)
        if chat_id == session.get('chat'):
            session['chat'] = None
        ses.commit()
        return redirect('/messanger')
    

@app.route('/add_user/<chat_id>')
def add_user(chat_id):
    with db_session.create_session as ses:
        chat = ses.get(models.Chat, chat_id)
        user = ses.get(models.User, current_user.id)
        potential_users = user.not_in_chat_friends(chat)
        return redirect('/messanger', potential_users=potential_users)


@app.route('/leave_chat/<chat_id>')
def leave_chat(chat_id):
    with db_session.create_session() as ses:
        chat = ses.get(models.Chat, chat_id)
        chat.users.remove(ses.get(models.User, current_user.id))
        if chat_id == session.get('chat'):
            session['chat'] = None
        ses.commit()
        return redirect('/messanger')


@app.route('/comments_chat/<chat_id>')
def comments_chat(chat_id):
    with db_session.create_session() as ses:
        chat = ses.get(models.CommentsChat, chat_id)
        chat.users.append(ses.get(models.User, current_user.id))
        ses.commit()
        session['chat'] = chat.id
        return redirect('/messanger')


# friends

@app.route('/friends')
@login_required
def friends():
    with db_session.create_session() as ses:
        user = ses.get(models.User, current_user.id)
        friends = user.friends
        # It's five random non friend users, just trust me.
        users = ses.query(models.User).filter(
            models.User.id.notin_([x.user2_id for x in friends]), 
            models.User.id != current_user.id).all()
        users = random.sample(users, k=min(len(users), 5))
        return render_template('friends.jinja', title='Friends', user=user, friends=friends, users=users)


@app.route('/add_friend/<id>')
@login_required
def add_friend(id):
    with db_session.create_session() as ses:
        
        user = ses.get(models.User, id)
        cur_user = ses.get(models.User, current_user.id)
        friends1 = models.Friends()
        friends1.user1_id = user.id
        friends1.user2_id = cur_user.id

        friends2 = models.Friends()
        friends2.user1_id = cur_user.id
        friends2.user2_id = user.id

        chat = models.Chat(name=f'{cur_user.short_name} and {user.short_name}')
        chat.users.append(cur_user)
        chat.users.append(user)
        friends1.dialog = chat
        friends2.dialog = chat
        ses.add(friends1)
        ses.add(friends2)
        ses.commit()
        return redirect('/friends')


@app.route('/to_chat/<user_id>')
def to_chat(user_id):
    with db_session.create_session() as ses:
        user = ses.get(models.User, user_id)
        friends = ses.query(models.Friends).filter(models.Friends.user1_id == current_user.id, 
                                                   models.Friends.user2_id == user.id).first()
        session['chat'] = friends.dialog.id
        return redirect('/messanger')


# other

@app.route('/')
def index():
    if isinstance(current_user, AnonymousUserMixin):
        return redirect('/login')
    session['last_page'] = '/'
    with db_session.create_session() as ses:
        user = ses.get(models.User, current_user.id)
        return render_template('wall.jinja', title='Main Page', user=user)


@app.route('/like/<post_id>')
def like(post_id):
    with db_session.create_session() as ses:
        post = ses.get(models.Post, post_id)
        user = ses.get(models.User, current_user.id)
        post.likes.append(user)
        ses.commit()
        return redirect(session['last_page'])   


def main():
    db_session.global_init('db/db.db')
    app.run(port=8080, host='localhost', debug=True)


if __name__ == '__main__':
    main()
