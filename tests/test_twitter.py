from __future__ import absolute_import, division, print_function
import os.path
import pytest
import app.twitter
try:
    from dotenv import load_dotenv
except ImportError:
    pass

try:
    dotenv_path = os.path.abspath(os.path.join(os.path.pardir, "local_setup.py"))
    load_dotenv(dotenv_path)
except FileNotFoundError:
    pass

consumer_key = os.environ["CONSUMER_API_KEY"]
consumer_secret = os.environ["CONSUMER_API_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]


@pytest.fixture
def me():
    me = app.twitter.main()
    return me


def test_api_connection(me):
    assert me.id == 3004355500


def test_list_of_followers(me):
    assert me.followers_ids() == [855057222627454977, 2618262152,  4815210058, 800074851335536640,  3007769517,
                                  801998858775498752,  777810001888997376, 42554977,  39286720, 92269871]
