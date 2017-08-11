# Twitter followers of followers

[![Build Status](https://travis-ci.org/mdyzma/twitter_follo.svg?branch=master)](https://travis-ci.org/mdyzma/twitter_follo)
[![Documentation Status](https://readthedocs.org/projects/twitter-follo/badge/?version=latest)](http://twitter-follo.readthedocs.io/en/latest/?badge=latest)


A Python app, which can displays followers of the followers of account authorized via Twitter. Can be deployed to Heroku.

Application inspiredUI based on MDB Free and EBM Bootstrap Plugin, available under MIT License and provided by [MDBoostrap.com](https://mdbootstrap.com).

## Usage

1. Visit [web site](https://twitter-followers-prod.herokuapp.com)

[![start]][start](https://twitter-followers-prod.herokuapp.com)

2. Sign in with your Twitter account
3. Browse list of followers who follow followers :)

![followers][followers]

Data are also accssible in JSON format:

![followers_json][followers_json]



## Deploying to Heroku

To deploy your copy of application simply click:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

(you will need Twitter app and SECRET CREDENTIALS provided by Twitter in order to make it work)

You can also quickly deploy using git. Make sure you have [HerokuCLI][HerokuCLI] installed.

```sh
$ git clone https://github.com/mdyzma/twitter_follo.git
$ cd twitter_follo
$ heroku create
$ git push heroku master
$ heroku open
```


## Running Locally

It can be also run locally. Make sure you have [Python][Python] and [HerokuCLI][HerokuCLI].

```sh
$ git clone https://gitlab.com/mdyzma/twitter_follo.git
$ cd twitter_follo
$ pip install --no-cache-dir -r requirements.txt

$ heroku local
```

Your app should now be running on [http://127.0.0.1:5000](http://localhost:5000/).






## Documentation

For more information, i.e. about app further development, see the documentation [Twitter Followers](http://twitter-follo.readthedocs.io/en/latest/?badge=latest)

<!-- Links -->
[Python]:    http://install.python-guide.org
[HerokuCLI]: https://toolbelt.heroku.com

<!-- Images -->

[start]:     static/img/screen-start.png
[followers]: static/img/screen-followers.png
[followers_json]: static/img/screen-followers-json.png
