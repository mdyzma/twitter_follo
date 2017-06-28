from flask import (Flask, flash, request, redirect, render_template, session, url_for)

import auth


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("base.html")


@app.route('/index')
def start():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
