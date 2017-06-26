# Twitter followers followers

[![build status](https://gitlab.com/mdyzma/twitter_follo/badges/master/build.svg)](https://gitlab.com/mdyzma/twitter_follo/commits/master) 
[![coverage report](https://gitlab.com/mdyzma/twitter_follo/badges/master/coverage.svg)](https://gitlab.com/mdyzma/twitter_follo/commits/master)


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

- [Twitter Followers](https://devcenter.heroku.com/categories/python)
