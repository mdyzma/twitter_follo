#!/usr/bin/env python
"""OAuth module giving additional layer of abstraction to the oauth library."""

# -----------------------------------------------------------------------------
# Standard Library Imports
# -----------------------------------------------------------------------------
from __future__ import absolute_import
import sys
import os.path
import time
import pickle
import math
from abc import abstractmethod
# -----------------------------------------------------------------------------
# Related Library Imports
# -----------------------------------------------------------------------------
from rauth import OAuth1Service
from flask import current_app, url_for, request, redirect, session
# -----------------------------------------------------------------------------
# Local Library Imports
# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
# Maximal amount of followers ids returned by Twitter API.

sys.path.insert(0, os.path.abspath('.'))


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    @abstractmethod
    def authorize(self):
        pass

    @abstractmethod
    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class TwitterSignIn(OAuthSignIn):
    """Subclass expanding general SignIn for twitter API.
    """
    def __init__(self):
        super(TwitterSignIn, self).__init__('twitter')
        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/'
        )

    def authorize(self):
        request_token = self.service.get_request_token(
            params={'oauth_callback': self.get_callback_url()}
        )
        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    def callback(self):
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return None, None, None, None
        oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']}
        )

        # Verify user GET request
        me = oauth_session.get('account/verify_credentials.json').json()

        # Info for database
        social_id = str(me.get('id'))
        username = me.get('screen_name')
        followers_count = me.get('followers_count')

        followers_data = {}#get_all(social_id, oauth_session)

        return social_id, username, followers_count, followers_data


def get_current_limits(oauth_session):
    """Function returns current lookups status via Twitter API call

    """
    temp = oauth_session.get('application/rate_limit_status.json?resources=help,users,search,statuses').json()
    lookups = temp["resources"]["users"]["/users/lookup"]["remaining"]
    follower_ids = temp["resources"]["followers"]["/followers/ids"]["remaining"]
    return follower_ids, lookups


def get_all(social_id, oauth_session):
    
    # user_data = oauth_session.get('users/show.json?user_id={}'.format(social_id)).json()
    # Get followers from the first page
    followers_list = oauth_session.get('followers/ids.json?cursor=-1&user_id={}&count=5000'.format(social_id)).json()

    # User Lookup of fetched followers list for thir account details, 100 at one time
    lookup_data = []
    if len(followers_list) > 100:
        chunks = [followers_list[x:x+100] for x in range(0, len(followers_list), 100)]
        
        for chunk in chunks:
            lookup_data += oauth_session.get('users/lookup.json?user_id={}'.format(expand_list_to_param(chunk)))
    else:
        lookup_data = oauth_session.get('users/lookup.json?user_id={}'.format(expand_list_to_param(followers_list)))
  
    # get list of followers sorted descending in respect to followers amount
    sorted_list = sort_followers(lookup_data)
    # TODO extract additional info from lookup to fill database with screen names
    # Check limits
    _idslimit, _lookuplimit = get_current_limits(oauth_session)
    
    # adjust list to the top 15 followers from the first page
    sorted_list = sorted_list[:_idslimit]
    data = {}
    for item in sorted_list:
        sub_list = oauth_session.get('followers/ids.json?cursor=-1&user_id={}&count=5000'.format(item)).json()
        # TODO page lookup of all 2nd followers, not only first page
        data[item] = sub_list
    return data


def expand_list_to_param(item_list):
    """Expands each python list to the string of arguments joined with coma."""
    if item_list:
        return ','.join([str(i) for i in item_list])


def sort_followers(lookup_response):
    """Using lookup data sorts list of followers in descending order"""
    _data = {}
    for element in lookup_response:
        fid, count = element.id, element.followers_count
        _data[fid] = count
    return [(key, val) for (key, val) in sorted(_data.items(), key=lambda x: x[1], reverse=True)]
