from __future__ import absolute_import, division, print_function

import os.path

import pytest

import auth

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
def api():
    api = auth.main()
    me = api.get_user(id=3004355500)
    return me


def test_api_connection(api):
    assert api.id == 3004355500


# def test_list_of_followers(me):
#     assert 855057222627454977 in me.followers_ids()
