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
from flask import current_app
# -----------------------------------------------------------------------------
# Local Library Imports
# -----------------------------------------------------------------------------


class Followers(object):

    CACHE_DIR = os.path.abspath(os.path.join(os.path.basename(__file__), '.cache'))

    """Followers of Follower class, collection of attributes and methods which
    intake account verification credentials json returned by server to collect
    info, which can  be used further in other modules. Once user is authenticated
    it will collect several info about his followers.

    Attributes
    ----------
    
    Note
    ----
    Data structure saved to cache::
        
        {
        "id": 877242472912564224
        "screen_name": "TEDxSingapore"
        "followers_count": 0,
        "followers_ids": [
        ...
        ],
        }
    
        
    """

    def __init__(self, auth_user=None, service=None):
        # User data

        self.auth_user = auth_user
        self.service = service
        self.uid = self.auth_user.get('id')
        self.screen_name = self.auth_user.get('screen_name')
        self.followers_count = self.auth_user.get('followers_count')

        # Cache dir
        if not os.path.exists(Followers.CACHE_DIR):
            os.makedirs(Followers.CACHE_DIR)
        self.cache_file_list = self.list_cache()

        # Twitter API
        if self.service:
            # Data produced by API calls
            self.followers_list = self.get_followers_list(self.uid)
            self.lookup_response = self.lookup_users()
            self.sorted_followers_list = self.sort_followers_list()
        else:
            current_app.logger.error('Not authorized to use Twitter API.')

# ----------------------------------------------------------------------------
# API requests
# ----------------------------------------------------------------------------
    def get_current_limits(self):
        """Function returns current lookups status via Twitter API call.
        """
        temp = self.service.get('application/rate_limit_status.json')

        lookups = temp.data.get("resources").get("users").get("/users/lookup").get("remaining")
        follower_ids = temp.data.get("resources").get("followers").get("/followers/ids").get("remaining")
        return follower_ids, lookups

    def get_followers_list(self, _uid):
        _resp = self.service.get('followers/ids.json', data={'user_id': _uid, 'count': 5000})
        return _resp.data.get('ids')


    def lookup_users(self, followers_list):
        """Looks up profile data of authenticated user followers. Useful to sort
        in respect to followers count. This way first 14 GET requests is able to
        gather largest lists.

        _ note:: Maximal length of lookup list is 100 id at one. One can have
        900 lookups per 15 min, which gives 90 000 data sets. If Followers count
        is bigger than 90 000 entire operation will take more than 15 min.
        """

        lookup_data = []
        _, _lookups = Followers.get_current_limits()

        if _lookups*100 > followers_list:
            pass
        # TODO Large datasets in pages

        # API accepts max 100 ids at the time, while get id returns 5000,
        # therefore 50 lookups can be done for account with 5000 followers
        if len(followers_list) > 100:
            chunks = [followers_list[x:x+100] for x in range(0, len(followers_list), 100)]

            for chunk in chunks:
                lookup_data.append(self.service.get('users/lookup.json',
                                                    data={'user_id': '{}'.format(Followers.expand_list_to_param(chunk))}).data)
        else:
            lookup_data = self.service.get('users/lookup.json',
                                           data={'user_id': '{}'.format(Followers.expand_list_to_param(followers_list))}).data

        return lookup_data

    def get_second_followers(self):
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
        # TODO waiting time check
        # adjust list to the top largest followers, limited with 'GET followers/ids' API limit. If list is larger
        #  than 5000, takes first page
        data = {}

        _sorted = self.sorted_followers_list[:_idslimit]

        for follower in _sorted:
            _resp = self.get_followers_list(follower)
            _lookup = self.lookup_users(_resp)

            for user in self.lookup_response:
                if follower in user.get('id'):
                    data = {'id': follower,
                            'name': user.get('screen_name'),
                            'followers_count': user.get('followers_count'),
                            'followers_ids': _resp}
        return data


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

        return [key for (key, val) in sorted(_data.items(), key=lambda x: x[1], reverse=True)]

    @staticmethod
    def expand_list_to_param(item_list):
        """Expands each python list to the string of arguments joined with coma.
        Used to create proper calls to bulk lookup of users."""
        if item_list:
            return ','.join([str(i) for i in item_list])

    def who_is_following_who(self):
        pass
# ----------------------------------------------------------------------------
# I/O OPERATIONS
# ----------------------------------------------------------------------------

    def list_cache(self):
        fspec = os.path.join(Followers.CACHE_DIR, '*.json')
        self.cache_file_list = [i for i in glob(fspec)]
        return self.cache_file_list

    @staticmethod
    def is_cache_empty():
        """Are there any JSON files in cache"""
        fspec = os.path.join(Followers.CACHE_DIR, '*.json')

        flist = [i for i in glob(fspec)]
        if len(flist) == 0:
            return True
        return False

    def clear_cache(self):
        pass

    def read_cache(self):
        pass

    def save_json(self, data):
        fname = os.path.join(Followers.CACHE_DIR, '_'.join([self.uid, 'followers']))
        with open(fname, 'w') as f:
            f.write(json.dumps(data, indent=4))

    def __repr__(self):
        _msg = "Follower: {} id: {}".format(self.screen_name, id(__class__))
        return _msg


def main():
    pass

if __name__ == '__main__':
    main()
