from __future__ import absolute_import, division, print_function
import tweepy
import logging # TODO add logging to the programm

from local_settings import (CONSUMER_API_KEY, CONSUMER_API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# TODO move to environment variables


consumer_key = str(CONSUMER_API_KEY)
consumer_secret = str(CONSUMER_API_SECRET)
access_token = str(ACCESS_TOKEN)
access_token_secret = str(ACCESS_TOKEN_SECRET)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)





# TODO api oAuth return

# TODO Get followers follower of indicated  and return list


def _print_report(user_obj, followers_list):
    print("Name: {}".format(user_obj.name))
    print("Screen Name: {}".format("".join(["@", user_obj.screen_name])))
    print("Created at: {}".format(user_obj.created_at.isoformat()))
    print()
    print("Followers:")
    print("-"*60)
    print("{:20}{:20}{:>20}".format("id", "@handle", "# of followers"))
    print("-"*60)
    for follower in followers_list:
        print("{:20}{:20}{:20}".format(follower.id_str, "".join(["@", follower.screen_name]),
              follower.followers_count))
    print("-"*60)
    print("\n\n")


def main():
    api = tweepy.API(auth)
    me = api.get_user(id=3004355500)
    me_followers = me.followers()

    _print_report(me, me_followers)

if __name__ == "__main__":
    main()
