from __future__ import absolute_import, division, print_function

import pytest
import app.twitter
from local_settings import *

@pytest.fixture
def me():
    import tweepy

    consumer_key = str(CONSUMER_API_KEY)
    consumer_secret = str(CONSUMER_API_SECRET)
    access_token = str(ACCESS_TOKEN)
    access_token_secret = str(ACCESS_TOKEN_SECRET)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    me = api.get_user(id=3004355500)
    return me


def test_api_connection(me):
    assert me.id == 3004355500