from __future__ import absolute_import, print_function

import os

from flask import Flask, render_template

from .base_routes import base
from .routes_v1.routes import routes_v1

app = Flask(__name__,
            static_folder=os.path.join(os.getcwd(), 'static'),
            static_url_path='',
            template_folder=os.path.join(os.getcwd(), 'templates'),
            )
app.config['DEBUG'] = False

app.register_blueprint(base)
app.register_blueprint(routes_v1)

@app.route('/routes/')
def routes():
    post_routes = []
    get_routes = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods:
            get_routes.append(rule)     #.rule)
        if "POST" in rule.methods:
            post_routes.append(rule)    #.rule)

    return render_template('routes.html', get_routes=get_routes, post_routes=post_routes)


