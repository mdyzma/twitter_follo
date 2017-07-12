# from __future__ import absolute_import, division, print_function

# import os.path
# import pytest

# try:
#     from dotenv import load_dotenv
# except ImportError:
#     pass

# try:
#     dotenv_path = os.path.abspath(os.path.join(os.path.pardir, "local_setup.py"))
#     load_dotenv(dotenv_path)
# except FileNotFoundError:
#     consumer_key = os.environ["CONSUMER_API_KEY"]
#     consumer_secret = os.environ["CONSUMER_API_SECRET"]
#     access_token = os.environ["ACCESS_TOKEN"]
#     access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]


# @pytest.fixture()
# def app():
#     app = create_app()
#     return app


# def test_app_basic(app):
#     pass
