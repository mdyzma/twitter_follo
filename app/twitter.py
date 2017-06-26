from __future__ import absolute_import, division, print_function
import os.path
import logging # TODO add logging to the programm
from dotenv import load_dotenv
import tweepy


try:
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname("."), 'local_settings.py'))
    load_dotenv(dotenv_path)
except FileNotFoundError:
    pass


consumer_key = os.environ["CONSUMER_API_KEY"]
consumer_secret = os.environ["CONSUMER_API_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]


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
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    me = api.get_user(id=3004355500)
    return me




if __name__ == "__main__":
    me = main()
    me_followers = me.followers()
    _print_report(me, me_followers)