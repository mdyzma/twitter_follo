"""Main Follower class implementation application. Dynamically routs between views."""

# -----------------------------------------------------------------------------
# Standard Library Imports
# -----------------------------------------------------------------------------
from __future__ import absolute_import
import os
import json
from glob import glob
# -----------------------------------------------------------------------------
# Related Library Imports
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Local Library Imports
# -----------------------------------------------------------------------------


class Followers(object):

    """Followers of Follower class, collection of attributes and methods which
    intake account verification credentials json returned by server to collect
    info, which can  be used further in other modules. Once user is authenticated
    it will collect several info about his followers.

    Attributes
    ----------
    """

    def __init__(self, auth_user=None, service=None):
        self.auth_user = auth_user
        self.service = service
        self.uid = self.auth_user.get('id')
        self.screen_name = self.auth_user.get('screen_name')
        self.followers_count = self.auth_user.get('followers_count')
        
        if self.service:
            self._current_limits = Followers.get_current_limits(self.service)
            # Data produced by API calls
            self.followers_list = self.get_followers_list()
            self.lookup_response = self.lookup_users()
            self.sorted_followers_list = self.sort_followers_list()
            self._followers_json = {}


# ----------------------------------------------------------------------------
# DATA MANIPULATIONS
# ----------------------------------------------------------------------------
    def sort_followers_list(self):
        """Using lookup data sorts list of current user followers in descending
        order by number of followers for each.

        Returns
        -------
        list
            Sorted list of followers.
        """
        _data = {}
        for element in self.lookup_response:
            fid, count = element.get('id'), element.get('followers_count')
            _data[fid] = count

        return [(key, val) for (key, val) in sorted(_data.items(), key=lambda x: x[1], reverse=True)]
# ----------------------------------------------------------------------------
# API contacts
# ----------------------------------------------------------------------------

    def get_current_limits(self):
        """Function returns current lookups status via Twitter API call.
        """
        temp = self.service.get('application/rate_limit_status.json')

        lookups = temp.data.get("resources").get("users").get("/users/lookup").get("remaining")
        follower_ids = temp.data.get("resources").get("followers").get("/followers/ids").get("remaining")
        return follower_ids, lookups
    
    def get_followers_list(self):
        _resp = self.service.get('followers/ids.json', data={'user_id': self.uid, 'count': 5000})
        return _resp.data.get('ids')


    
    def lookup_users(self):
        """Looks up profile data of authenticated user followers. Useful to sort
        in respect to followers count. This way first 14 GET requests is able to
        gather largest lists.

        _ note:: Maximal length of lookup list is 100 id at one. One can have
        900 lookups per 15 min, which gives 90 000 data sets. If Followers count
        is bigger than 90 000 entire operation will take more than 15 min.
        """

        lookup_data = []
        _, _lookups = Followers.get_current_limits()

        if _lookups
        if len(self.followers_list) > 100:
            chunks = [self.followers_list[x:x+100] for x in range(0, len(self.followers_list), 100)]

            for chunk in chunks:
                lookup_data.append(self.service.get('users/lookup.json',
                                                    data={'user_id': '{}'.format(Followers.expand_list_to_param(chunk))}).data)
        else:
            lookup_data = self.service.get('users/lookup.json',
                                           data={'user_id': '{}'.format(Followers.expand_list_to_param(self.followers_list))}).data
        
        return lookup_data

    def get_all(self):
        """Gets list of followers for authenticated user and crawl one by one
        to get list of second degree followers for each item from previous list.
        If followers count exceeds 5000, due toT Twitter API limitations only
        first page (counting 5000 items) is downloaded.

        Arguments
        ---------

        Returns
        -------
        dict
            dictionary of authenticated user followers as keys and list of followers
            for each key.
        """

        # Check limits
        _idslimit, _ = Followers.get_current_limits()
        # TODO waiting time chack
        # adjust list to the top largest followers, limited with 'GET followers/ids' API limit. If list is larger
        #  than 5000, takes first page
        data = {}

        _sorted = self.sorted_followers_list[:_idslimit]

        for follower in _sorted:
            resp = self.service.get('followers/ids.json',
                                    data={'cursor': -1, 'user_id': follower, 'count': 5000}).data

            data[follower] = resp.get('ids')
            return data



    @staticmethod
    def expand_list_to_param(item_list):
        """Expands each python list to the string of arguments joined with coma.
        Used to create proper calls to bulk lookup of users."""
        if item_list:
            return ','.join([str(i) for i in item_list])

    def __repr__(self):
        _msg = "Follower: {} id: {}".format(self.screen_name, id(__class__))
        return _msg
