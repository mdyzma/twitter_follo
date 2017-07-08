.. _development:

Twitter Followers Workflow
==========================


This document contains some best practices, and basic workflow which can be used during further Twitter Followers app development. 

Start
-----

If you want to try this example, follow this steps:

1. Clone or download the project's repository: `GitHub <https://github.com/mdyzma/twitter_follo>`_
2. Create a virtual environment and install packages from the requirements.txt file (you can use Python 2.7 or 3.5+).
3. Register "app" with Twitter on `https://apps.twitter.com <https://apps.twitter.com>`_.
4. Update local_settings.py with the ids and secret codes of your Twitter app.
5. Run app locally


Clone or fork repository
------------------------

Get source files from Git repository from the server ::

    $ git clone https://gitlab.com/mdyzma/twitter_follo.git




Virtual environment and dependencies
------------------------------------

It is a good practice to develop project in clean environment, to control all dependencies. This step requires Python and virtualenv package to be present in your system Python installation. Install ``virtualenv`` using python package manager. ::
    
    $ pip install virtualenv -U

It is also good to keep your environments away from the project folder. it helps to avoid having large folders (i.e. python envs with installed dependencies, sometimes hundreds of MB) included in version control system. Usually I create one hidden folder in my users home directory i.e. ``.envs/`` and place all virtual environments for each project there. ::
    
    $ mkdir ~/.envs
    $ virtualenv ~/.envs/twitter

This will create python virtual environment with the specified name in ``.envs`` folder located in users home directory (Linux only). Check how to manage virtualenvs on windows OS `here <https://virtualenv.pypa.io/en/stable/userguide/#activate-script>`_


To activate it ::
    
    $ source ~/.envs/bin/activate

    (twitter) $

Prompt should change and be preceded with the environment name in parenthesis. Once fresh environment is ready it is time to install development dependencies::
    
    (twitter) $ pip install --no-cache-dir -r requirements/dev.txt




Continuous Integration
----------------------

Project can be easly connected to CI service like TravisCI or CircleCI and authomaticaly run tests and deploy code to Heroku. Github repository can be also be directly connected to Heroku service. In that case All services will sense specified git branch changes and runjobs specified in configuration file. 

Configuration file for TravisCI is located in project's root directory: ``travis-ci.yml`` ::
    
    language: python
        python:
            - "2.7"
            - "3.5"
            - "3.6"
            - "nightly" # currently points to 3.7-dev
    # command to install dependencies
    install: "pip install -r requirements.txt"
    
    # command to run tests and coverage report
    script: python -m pytest --cov-report xml --cov=app tests/
    script: codecov

    deploy:
        provider: heroku
    api_key:
        secure: "API-key-provided-by-heroku"
    
    app: fast-forest-95874



.. warning::
    Replace API key and name of the app with our own.




Manual Testing
--------------

Application is developed in Ext programming approach (extremely late working hours). Tests are grouped in root folder in ``tests/``. Tests use ``pytest`` module.

To run entire suite use ::
    
    (tweeter) $ python -m pytest --cov=src tests/


Output similar to this will appear ::
    
    ============================= test session starts =============================
    platform linux2 -- Python 2.7.13, pytest-3.1.0, py-1.4.33, pluggy-0.4.0
    rootdir: /home/mdyzma/projects/twitter_follo, inifile:
    plugins: cov-2.3.1
    collected 1 items

    tests/test_twitter.py E

    =================================== ERRORS ====================================
    ____________________ ERROR at setup of test_api_connection ____________________

        @pytest.fixture
        def api():
    >       api = auth.main()
    E       AttributeError: 'module' object has no attribute 'main'

    tests/test_twitter.py:28: AttributeError
    =========================== 1 error in 0.53 seconds ===========================
    ERROR: Failed to generate report: No data to report.


First run of test SHOULD fail. Use the force of TDD to make it nice and green.

For pretty html report add flag ::
    
    (twitter) $ python -m pytest --cov-report html --cov=src`

The later will produce nicely formatted report in ``htmlcov/`` folder.



Code quality
------------

I use PyCharm built-in pylint, but there is ``pylint`` module in python, which shows where code deviates from the official guidelines. See typical report::

    (twitter) $ pylint --report=y app.py
    
    pylint --reports=y app.py
    No config file found, using default configuration
    ************* Module twitter_follo.app
    C:  1, 0: Missing module docstring (missing-docstring)
    E:  3, 0: Unable to import 'flask_sqlalchemy' (import-error)
    E:  4, 0: Unable to import 'flask_login' (import-error)
    C:  8, 0: Invalid constant name "app" (invalid-name)
    C: 11, 0: Invalid constant name "consumer_key" (invalid-name)
    C: 12, 0: Invalid constant name "consumer_secret" (invalid-name)
    C: 13, 0: Invalid constant name "callback_url" (invalid-name)
    C: 15, 0: Invalid constant name "db" (invalid-name)
    C: 16, 0: Invalid constant name "lm" (invalid-name)
    C: 19, 0: Invalid constant name "session" (invalid-name)
    C: 20, 0: Invalid constant name "data" (invalid-name)
    C: 22, 0: Missing class docstring (missing-docstring)
    C: 24, 4: Invalid class attribute name "id" (invalid-name)
    R: 22, 0: Too few public methods (0/2) (too-few-public-methods)
    W: 31,14: Redefining built-in 'id' (redefined-builtin)
    C: 31, 0: Invalid argument name "id" (invalid-name)
    C: 31, 0: Missing function docstring (missing-docstring)
    C: 36, 0: Missing function docstring (missing-docstring)
    C: 41, 0: Missing function docstring (missing-docstring)
    C: 52, 0: Missing function docstring (missing-docstring)
    C: 78, 0: Missing function docstring (missing-docstring)
    W:  4, 0: Unused login_user imported from flask_login (unused-import)
    W:  4, 0: Unused logout_user imported from flask_login (unused-import)
    W:  4, 0: Unused current_user imported from flask_login (unused-import)
    
    
    Report
    ======
    52 statements analysed.
    
    Statistics by type
    ------------------
    
    +---------+-------+-----------+-----------+------------+---------+
    |type     |number |old number |difference |%documented |%badname |
    +=========+=======+===========+===========+============+=========+
    |module   |1      |1          |=          |0.00        |0.00     |
    +---------+-------+-----------+-----------+------------+---------+
    |class    |1      |1          |=          |0.00        |0.00     |
    +---------+-------+-----------+-----------+------------+---------+
    |method   |0      |0          |=          |0           |0        |
    +---------+-------+-----------+-----------+------------+---------+
    |function |5      |5          |=          |0.00        |0.00     |
    +---------+-------+-----------+-----------+------------+---------+
    
    
    
    External dependencies
    ---------------------
    ::
    
        auth (twitter_follo.app)
        flask (twitter_follo.app)
        tweepy (twitter_follo.app)
    
    
    
    Raw metrics
    -----------
    
    +----------+-------+------+---------+-----------+
    |type      |number |%     |previous |difference |
    +==========+=======+======+=========+===========+
    |code      |58     |69.05 |NC       |NC         |
    +----------+-------+------+---------+-----------+
    |docstring |0      |0.00  |NC       |NC         |
    +----------+-------+------+---------+-----------+
    |comment   |3      |3.57  |NC       |NC         |
    +----------+-------+------+---------+-----------+
    |empty     |23     |27.38 |NC       |NC         |
    +----------+-------+------+---------+-----------+
    
    
    
    Duplication
    -----------
    
    +-------------------------+------+---------+-----------+
    |                         |now   |previous |difference |
    +=========================+======+=========+===========+
    |nb duplicated lines      |0     |0        |=          |
    +-------------------------+------+---------+-----------+
    |percent duplicated lines |0.000 |0.000    |=          |
    +-------------------------+------+---------+-----------+
    
    
    
    Messages by category
    --------------------
    
    +-----------+-------+---------+-----------+
    |type       |number |previous |difference |
    +===========+=======+=========+===========+
    |convention |17     |17       |=          |
    +-----------+-------+---------+-----------+
    |refactor   |1      |1        |=          |
    +-----------+-------+---------+-----------+
    |warning    |4      |4        |=          |
    +-----------+-------+---------+-----------+
    |error      |2      |2        |=          |
    +-----------+-------+---------+-----------+
    
    
    
    Messages
    --------
    
    +-----------------------+------------+
    |message id             |occurrences |
    +=======================+============+
    |invalid-name           |10          |
    +-----------------------+------------+
    |missing-docstring      |7           |
    +-----------------------+------------+
    |unused-import          |3           |
    +-----------------------+------------+
    |import-error           |2           |
    +-----------------------+------------+
    |too-few-public-methods |1           |
    +-----------------------+------------+
    |redefined-builtin      |1           |
    +-----------------------+------------+
    
    
    
    
    ------------------------------------------------------------------
    Your code has been rated at 3.85/10 (previous run: 3.85/10, +0.00)


Documentation
-------------

For documentation reStructuredText plain text markup syntax is used. It is an easy-to-read, what-you-see-is-what-you-get markup, with large capabilities to automate documentation creation, or include it into CI pipeline.

To regenerate documentation after some changes cd to docs/ folder and type::

    $ make html

Static web page will be created from ``*.rst`` files located in ``source/`` directory. Location of main static site is: ``docs/build/html/index.html``. It works much better if it is served (it uses some basic javascript). Therefore there are two options. 

1. Run external software to serve www (apache, nginx)
2. use built in python server from html folder. 

There is also third possibility, which may be much better in case of large documentation updates. Install ``sphinx-autobuild`` ::
    
    $ pip install sphinx-autobuild


Enter docs folder and run local server, which will rerun sphinx build process when it detects changes in ``.rst`` files. To start server type::
    
    (twitter) $ sphinx-autobuild docs\source docs\build\html

    +--------- manually triggered build ---------------------------------------------
    | Running Sphinx v1.6.2
    | loading pickled environment... failed: unsupported pickle protocol: 4
    | building [mo]: targets for 0 po files that are out of date
    | building [html]: targets for 6 source files that are out of date
    | updating environment: 6 added, 0 changed, 0 removed
    | reading sources... [ 16%] api
    | reading sources... [ 33%] contribution
    | reading sources... [ 50%] development
    | reading sources... [ 66%] index
    | reading sources... [ 83%] license
    | reading sources... [100%] quickstart
    |
    | looking for now-outdated files... none found
    | pickling environment... done
    | checking consistency... done
    | preparing documents... done
    | reading sources... [ 16%] api
    | reading sources... [ 33%] contribution
    | reading sources... [ 50%] development
    | reading sources... [ 66%] index
    | reading sources... [ 83%] license
    | reading sources... [100%] quickstart
    |
    | generating indices... genindex
    | writing additional pages... search
    | copying static files... done
    | copying extra files... done
    | dumping search index in English (code: en) ... done
    | dumping object inventory... done
    | build succeeded.
    +--------------------------------------------------------------------------------
    
    [I 170522 13:12:16 server:283] Serving on http://127.0.0.1:8000
    [I 170522 13:12:16 handlers:60] Start watching changes
    [I 170522 13:12:16 handlers:62] Start detecting changes


To extract doctrings from source code `sphinx autodoc <http://www.sphinx-doc.org/en/stable/ext/autodoc.html>`_ extension is used. Default docstring format is numpydoc. To parse it properly `napoleon project <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/>`_ is used.


To generate documentation based on source code doctstrings type::
    
    (twitter) $ sphinx-apidoc -f -o docs/source .

    Creating file docs/source/twitter_follo.rst.
    Creating file docs/source/modules.rst.
