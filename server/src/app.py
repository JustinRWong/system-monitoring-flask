from flask import Flask, Response, request, abort, jsonify, render_template, make_response, session, redirect
from flask_bootstrap import Bootstrap
import psutil
import json
import logging
import os

import requests
import time
from constants import *
from scheduler_tasks import *
'''
App setup
'''
def create_app(app, config=None):
    # load app sepcified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    # setup_app(app)

    # app.wsgi_app = SaferProxyFix(app.wsgi_app) # may not be needed
    return app

app = Flask(__name__)
Bootstrap(app)

scheduler = BackgroundScheduler()
scheduler.add_job(func=get_system_stats, trigger="interval", seconds=60)
scheduler.start()

###############################################
#             Init and confis our app         #
###############################################
app.jinja_env.cache = {}
app.config["CACHE_TYPE"] = "null"
if __name__ == '__main__':
    ## setup app
    app = create_app(app, {
        'SECRET_KEY': 'secret',
        'SQLALCHEMY_TRACK_MODIFICATIONS': True,
        # 'SQLALCHEMY_DATABASE_URI': DB_CONNECTION_STRING,
    })

    ## run web server
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

'''
App Routes
'''

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/')
def home():
    return render_template('index.html',
                            title="SYSTEM MONITOR WEB APP",
                            memory=IN_MEMORY_HISTORICAL_USAGE,
                            cpu_count=psutil.cpu_count())

@app.route('/historical')
def historical():
    # capture latest
    get_system_stats()
    # return all
    return jsonify([v for v in IN_MEMORY_HISTORICAL_USAGE.getall().values()])