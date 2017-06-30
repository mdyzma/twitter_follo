from __future__ import absolute_import, print_function
import os.path
# import logging # TODO add logging to the program
import tweepy
# import oauth2 as oauth


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


consumer_key = os.environ["CONSUMER_API_KEY"]
consumer_secret = os.environ["CONSUMER_API_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
