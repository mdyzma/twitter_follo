from __future__ import absolute_import, print_function
from flask import (Flask, flash, request, redirect, render_template, session, url_for)
import tweepy
import auth

app = Flask(__name__, static_folder='static')


consumer_key = auth.consumer_key
consumer_secret = auth.consumer_secret
callback_url = '0.0.0.0:5000/signin'

session = {}
data = {}


@app.route('/')
def index():
    return render_template('start.html')


@app.route('/signin', methods=['POST'])
def sign_in():
    oauth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
    try:
        url = oauth.get_authorization_url()
        session['request_token'] = oauth.request_token
    except tweepy.TweepError:
        flash('Error! Failed to get request token')
    return redirect(url)


@app.route("/verify")
def get_verification():
    # get the verifier key from the request url
    verifier = request.args['oauth_verifier']

    oauth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    token = session['request_token']
    del session['request_token']

    oauth.set_access_token(token[0], token[1])

    try:
        oauth.get_access_token(verifier)
    except tweepy.TweepError:
        flash('Error! Failed to get access token.')

    # now you have access!
    api = tweepy.API(oauth)

    # store data
    data['api'] = api
    data['access_token_key'] = oauth.access_token.key
    data['access_token_secret'] = oauth.access_token_secret
    return redirect(url_for('follower/follower'))


@app.route('/app')
def request_twitter():
    token, token_secret = session['token']
    oauth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
    oauth.set_access_token(token, token_secret)
    api = tweepy.API(oauth)
    return api.me()


@app.route('/follower/follower')
def followers(data):

    return render_template('start.html')


if __name__ == '__main__':
    app.run(debug=True)
