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
from flask import Flask, g, redirect, session, url_for, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, UserMixin, login_user, logout_user,
                         current_user, login_required)
from flask_oauthlib.client import OAuth
from flask_debugtoolbar import DebugToolbarExtension
# -----------------------------------------------------------------------------
# Local Library Imports
# -----------------------------------------------------------------------------
# from twitter_app.followers import Followers

# ----------------------------------------------------------------------------
# Read sensitive data
# ----------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
except ImportError:
    pass

try:
    # !! ALWAYS EXCLUDE THIS FILE FROM VERSION CONTROL !!
    dotenv_path = os.path.abspath('local_settings.py')  
    load_dotenv(dotenv_path)
except OSError:
    pass
finally:
    consumer_key = os.environ["CONSUMER_API_KEY"]
    consumer_secret = os.environ["CONSUMER_API_SECRET"]
    access_token = os.environ["ACCESS_TOKEN"]
    access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

# ----------------------------------------------------------------------------
# Setting flask app with user and 3 leg authorization
# ----------------------------------------------------------------------------
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'
toolbar = DebugToolbarExtension(app)
oauth = OAuth(app)


# Database User model 
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    fcount = db.Column(db.Integer, nullable=True)
    oauth_token = db.Column(db.String(200), nullable=True)
    oauth_secret = db.Column(db.String(200), nullable=True)

# TODO Move data to MONGO


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

# ----------------------------------------------------------------------------
#  Oauth init
# ----------------------------------------------------------------------------
twitter = oauth.remote_app(
    'twitter',
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize'
)


@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']   
    return resp['oauth_token'], resp['oauth_token_secret']


@app.before_request
def before_request():
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']


# ----------------------------------------------------------------------------
# views
# ----------------------------------------------------------------------------
@app.route('/')
def index():
    app.logger.info('App started.')
    return render_template('start.html')


@app.route('/login')
def login():
    callback_url = url_for('oauth_authorized', next=request.args.get('next'))
    # login_user()
    return twitter.authorize(callback=callback_url or request.referrer or None)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/oauth-authorized')
def oauth_authorized():
    """Authorization rout, which also gets data to the user table.

    Returns
    -------
    str
        Url to the callback url from Twitter ap settings

    """
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
        return redirect(url_for('index'))

    else:
        session['twitter_oauth'] = resp
        session['twitter_user'] = resp['screen_name']

    auth_user = twitter.get('account/verify_credentials.json')
    session['oauth_user'] = auth_user.data

    social_id = auth_user.data.get('id')
    username = auth_user.data.get('screen_name')
    followers_count = auth_user.data.get('followers_count')

    # Check if user is in db
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, fcount=followers_count,
                    oauth_token=resp['oauth_token'], oauth_secret=resp['oauth_token_secret'])
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('followers'))


@app.route('/followers/followers/', methods=['GET'])
def followers():
    app.logger.debug('Twitter authorization successful.')
    user_followers = None
    user_name = session['twitter_user']

    # Obtain verified user data

    _followers = twitter.get('followers/ids.json',
                             data={'cursor': -1, 'screen_name': user_name, 'count': 5000}).data

    print(_followers.get("ids"))

    # Followers(session['oauth_user'], twitter)
    # _lookup_data = twitter.get('users/lookup.json', data={'user_id': '')
    #
    # followers_data = FollowersOfFollower(auth_user.data, twitter)

    return render_template('followers.html', followers=user_followers, user=user_name)


if __name__ == '__main__':
    db.create_all()
    app.run()
