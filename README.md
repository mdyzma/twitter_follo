# Twitter followers followers

[![Build Status](https://travis-ci.org/mdyzma/twitter_follo.svg?branch=master)](https://travis-ci.org/mdyzma/twitter_follo)
[![Documentation Status](https://readthedocs.org/projects/twitter-follo/badge/?version=latest)](http://twitter-follo.readthedocs.io/en/latest/?badge=latest)



A Python app, which can display followers of the followers of account authorized via Twitter. Can be deployed to Heroku.


## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/).

```sh
$ git clone https://gitlab.com/mdyzma/twitter_follo.git
$ cd twitter_follo

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Documentation

For more information, see these articles:

- [Twitter Followers](http://twitter-follo.readthedocs.io/en/latest/?badge=latest)
