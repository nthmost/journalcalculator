from __future__ import print_function, absolute_import

from flask import Blueprint, render_template

from metapub import FindIt

from .utils import HTTP200, HTTP400, get_hostname
from .config import ENV, CONFIG, PKGNAME

base = Blueprint('base', __name__, template_folder='templates')

@base.route('/')
def home():
    return render_template('home.html') 

@base.route('/about')
def about():
    return render_template('about.html')

@base.route('/OK')
def OK():
    return HTTP200({ 'service': '%s' % PKGNAME, 
                     'ENV': '%s' % ENV,
                     'hostname': '%s' % get_hostname(),
                     'api_latest_version': CONFIG.get('api', 'latest_version'), 
                     'api_supported_versions': CONFIG.get('api', 'supported_versions'),
                   })

@base.route('/findit/<pmid>')
def findit(pmid):
    source = FindIt(pmid=pmid)
    outd = source.to_dict()
    outd['article'] = source.pma.to_dict()
    return HTTP200(outd)

