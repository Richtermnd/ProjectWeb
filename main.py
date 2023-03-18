from flask import Flask, url_for, render_template, redirect
from data import db_session

app = Flask(__name__)

# S - safety
app.config['SECRET_KEY'] = 'SECRET_KEY'


def main():
    db_session.global_init('db/db.db')
    app.run(port=8080, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()
