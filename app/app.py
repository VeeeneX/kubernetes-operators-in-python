# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2019 Grey Li
    :license: MIT, see LICENSE for more details.
"""
from flask import Flask

app = Flask(__name__)

# the minimal Flask application
@app.route('/')
def index():
    return '<h1>Hello, Outie!</h1>'

# dynamic route, URL variable default
@app.route('/severed', defaults={'name': 'Mark S.'})
@app.route('/severed/<name>')
def greet(name):
    f = open("secret.txt", "r")
    numbers = f.read() * 42
    return f"<body><h1>Hello, innie {name}!</h1><span>Here some numbers to be done at the end of quarter, for micro data refinement</span><p>{numbers}</p></body>"

if __name__ == "__main__":
    app.run(debug=True)