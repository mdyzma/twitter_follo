#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Standard Library Imports
# -----------------------------------------------------------------------------
from __future__ import absolute_import, print_function
import sys
import json
import os.path
# -----------------------------------------------------------------------------
# Related Library Imports
# -----------------------------------------------------------------------------
import pytest
# -----------------------------------------------------------------------------
# Local Library Imports
# -----------------------------------------------------------------------------
from twitter_app.followers import Followers
# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
SAMPLE_AUTH_RESPONSE = json.loads('{"id": 877242472912564224, "id_str": "877242472912564224", "name": "Michal", "screen_name": "FoloTwitt", "location": "", "description": "", "url": null, "entities": {"description": {"urls": []}}, "protected": false, "followers_count": 0, "friends_count": 1, "listed_count": 0, "created_at": "Tue Jun 20 19:11:18 +0000 2017", "favourites_count": 0, "utc_offset": null, "time_zone": null, "geo_enabled": false, "verified": false, "statuses_count": 0, "lang": "pl", "contributors_enabled": false, "is_translator": false, "is_translation_enabled": false, "profile_background_color": "F5F8FA", "profile_background_image_url": null, "profile_background_image_url_https": null, "profile_background_tile": false, "profile_image_url": "http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png", "profile_image_url_https": "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png", "profile_link_color": "1DA1F2", "profile_sidebar_border_color": "C0DEED", "profile_sidebar_fill_color": "DDEEF6", "profile_text_color": "333333", "profile_use_background_image": true, "has_extended_profile": false, "default_profile": true, "default_profile_image": true, "following": false, "follow_request_sent": false, "notifications": false, "translator_type": "none"}')


@pytest.fixture(scope="module")
def follower_class():
    obj = Followers(auth_user=SAMPLE_AUTH_RESPONSE)
    return obj


@pytest.mark.usefixtures("follower_class")
class TestFollower(object):

    def test_main_exists(self):
        assert follower_class

    def test_constructor_uid(self):
        assert 877242472912564224, follower_class.uid

    def test_constructor_screen_name(self):
        assert 'FoloTwitt', follower_class.screen_name

    def test_constructor_followers_count(self):
        assert 0, follower_class.follower_count

    def test_class_repr(self):
        assert "Running main class", print(follower_class)
