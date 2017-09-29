#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: leason
@time: 2017/9/8 14:09
"""
from flask import Flask
from flask_cors import CORS

from app.example import add

app = Flask(__name__)


CORS(app, supports_credentials=True)


@app.route("/", methods=['GET', 'POST'])
def test():
    data={
        "name": "leason",
        "des": "des",
    }
    result = add(data)
    print result
    return 'ok'


if __name__ =='__main__':

    app.run(host='0.0.0.0', port=8888, debug=True, threaded=True)