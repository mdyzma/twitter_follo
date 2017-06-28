from __future__ import absolute_import, division, print_function
import os.path
# import logging # TODO add logging to the program
import tweepy
# import oauth2 as oauth


try:
    from dotenv import load_dotenv
except ImportError:
    pass

try:
    dotenv_path = os.path.abspath('local_settings.py')
    load_dotenv(dotenv_path)
except FileNotFoundError:
    pass


consumer_key = os.environ["CONSUMER_API_KEY"]
consumer_secret = os.environ["CONSUMER_API_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

# consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
# access_token = oauth.Token(key=access_token, secret=access_token_secret)
# client = oauth.Client(consumer, access_token)

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
    return api

if __name__ == "__main__":
    main()
