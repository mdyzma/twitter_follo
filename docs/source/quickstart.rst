.. quickstart:

Quickstart
==========

A Python app, which can display followers of the followers of account authorized via Twitter. Can be deployed to Heroku.


Running Locally
---------------

Make sure you have Python_ installed properly.  Also, install the Heroku_. ::

    $ git clone https://gitlab.com/mdyzma/twitter_follo.git
    $ cd twitter_follo

    $ heroku local


Your app should now be running on `localhost:5000 <http://localhost:5000/>`_.

Deploying to Heroku
-------------------

You can also ::

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate
    $ heroku open


or use fast deploy button:

|Deploy|

Documentation
-------------

For more information, see the documentation_.






.. links

.. _Python: http://install.python-guide.org
.. _Heroku: https://toolbelt.heroku.com
.. _documentation: http://twitter-follo.readthedocs.io/en/latest/?badge=latest


.. |Deploy| image:: https://www.herokucdn.com/deploy/button.png
    :target: https://heroku.com/deploy
    :alt: Heroku deploy

