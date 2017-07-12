import os
import pytest
from flask import Flask, g



from flask import Flask as _Flask


class Flask(_Flask):
    testing = True
    secret_key = 'test key'


@pytest.fixture
def app():
    app = Flask(__name__)
    return app


# @pytest.fixture
# def app_ctx(app):
#     with app.app_context() as ctx:
#         yield ctx


# @pytest.fixture
# def req_ctx(app):
#     with app.test_request_context() as ctx:
#         yield ctx


# @pytest.fixture
# def client(app):
#     return app.test_client()