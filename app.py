from __future__ import absolute_import, print_function
from flask import (Flask, flash, g, request, redirect, render_template, session, url_for)
# import tweepy
from flask_oauthlib.client import OAuth
import secrets


app = Flask(__name__, static_folder='static')
app.debug = True
app.secret_key = 'development'

oauth = OAuth(app)

twitter = oauth.remote_app(
    'twitter',
    consumer_key=secrets.consumer_key,
    consumer_secret=secrets.consumer_secret,
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


@app.route('/')
def index():
    return render_template('start.html')



# @app.route('/authorize', methods=['POST'])
# def authorize():
#     oauth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
#     try:
#         url = oauth.get_authorization_url()
#         session['request_token'] = oauth.request_token
#     except tweepy.TweepError:
#         flash('Error! Failed to get request token')
#     return redirect(url)

#
# @app.route("/verify")
# def get_verification():
#     # get the verifier key from the request url
#     verifier = request.args['oauth_verifier']
#
#     oauth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
#     token = session['request_token']
#     del session['request_token']
#
#     oauth.set_access_token(token[0], token[1])
#
#     try:
#         oauth.get_access_token(verifier)
#     except tweepy.TweepError:
#         flash('Error! Failed to get access token.')
#
#     # now you have access!
#     api = tweepy.API(oauth)
#
#     # store data
#     data['api'] = api
#     data['access_token_key'] = oauth.access_token.key
#     data['access_token_secret'] = oauth.access_token_secret
#     return redirect(url_for('followers/followers'))


@app.route('/login')
def login():
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)


@app.route('/logout')
def logout():
    session.pop('twitter_oauth', None)
    return redirect(url_for('start'))


@app.route('/oauthorized')
def oauthorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    return redirect(url_for('followers'))

@app.route('/followers/followers')
def followers():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    return render_template('followers.html')


if __name__ == '__main__':
    app.run(debug=True)
