#!/usr/bin/env python

# -----------------------------------------------------------------------------
# Standard Library Imports
# -----------------------------------------------------------------------------
from __future__ import absolute_import, print_function
import sys
import os.path
# -----------------------------------------------------------------------------
# Related Library Imports
# -----------------------------------------------------------------------------
import pytest
# -----------------------------------------------------------------------------
# Local Library Imports
# -----------------------------------------------------------------------------
from twitter_app.followers import TwitterFollowers


@pytest.fixture
def api():
    api = TwitterFollowers.auth
    me = api.get_user(id=3004355500)
    return me


def test_tweepy_api(api):
    status, 



