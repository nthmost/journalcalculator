from __future__ import absolute_import, print_function

import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

# rename "skeleton" to name of your app
from journalcalculator.app_config import app
from journalcalculator.config import CFGDIR, ENV, PKGNAME, CONFIG

app.wsgi_app = ProxyFix(app.wsgi_app) 

def show_envs():
    relevant_envs = [ '%s_SERVICES_ENV' % PKGNAME.upper(), 
                      '%s_SERVICES_CONFIG_DIR' % PKGNAME.upper(),
                      '%s_SERVICES_DEBUG' % PKGNAME.upper()]
    print('Config files in %s' % CFGDIR)
    print('Using %s.ini' % ENV)
    print('Relevant environment variable settings:')
    print_tmpl = '     %s: %s'
    for env in relevant_envs:
        print(print_tmpl % (env, os.getenv(env, 'not set')))

if __name__=='__main__':
    show_envs()
    app.run(debug=True, host='0.0.0.0', port=int(CONFIG.get('flask', 'port')))

