#!/usr/bin/env python
"""Main Flask application. Dynamically routs between views."""

# -----------------------------------------------------------------------------
# Standard Library Imports
# -----------------------------------------------------------------------------
from __future__ import absolute_import
import os
import json
# -----------------------------------------------------------------------------
# Related Library Imports
# -----------------------------------------------------------------------------
from flask import Flask, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
# -----------------------------------------------------------------------------
# Local Library Imports
# -----------------------------------------------------------------------------
from twitter_app.oauth import OAuthSignIn
from twitter_app import follower
# dotenv package will set key: value environment variables for app. Same mechanism is used on
# heroku web, where os env variables are created. This way sensitive data are never exposed.
try:
    from dotenv import load_dotenv
except ImportError:
    pass

try:
    dotenv_path = os.path.abspath('local_settings.py')  # !! ALWAYS EXCLUDE THIS FILE FROM VERSION CONTROL !!
    load_dotenv(dotenv_path)
except FileNotFoundError:
    pass

finally:
    consumer_key = os.environ["CONSUMER_API_KEY"]
    consumer_secret = os.environ["CONSUMER_API_SECRET"]
    access_token = os.environ["ACCESS_TOKEN"]
    access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'twitter': {
        'id': consumer_key,
        'secret': consumer_secret
    }
}

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    fcount = db.Column(db.Integer, nullable=True)

# TODO Move data to MONGO


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('start.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, followers_count, followers_of_followers = oauth.callback()

    # for now save to file
    json.dump(followers_of_followers, open("followers_of_followers.json", 'w'))

    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, fcount=followers_count)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('followers'))


@app.route('/followers/followers/', methods=['GET'])
def followers():
    michal_followers = json.load(open("michal2nd.json"))
    # render followers of followers with Coursor
    # user = User.query.filter_by(social_id=social_id).first()
    return render_template('followers.html', followers=michal_followers)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
