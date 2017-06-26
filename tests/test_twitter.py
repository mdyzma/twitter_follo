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


def test_list_of_followers(me):
    assert me.followers_ids() == [855057222627454977, 2618262152,  4815210058, 800074851335536640,  3007769517,
                                  801998858775498752,  777810001888997376, 42554977,  39286720, 92269871]
