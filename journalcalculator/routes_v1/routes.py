from __future__ import absolute_import, print_function

import logging, json, os, sys

import configparser

from flask import Flask, request, redirect
from flask import Blueprint

from flask import stream_with_context, request, Response

from metapub import FindIt

routes_v1 = Blueprint('routes_v1', __name__, template_folder='templates')

from ..config import CONFIG, ENV, PKGNAME, DEBUG
from ..utils import HTTP200, HTTP400
from ..pubmed_tools import *

log = logging.getLogger('%s.routes_v1' % PKGNAME)


def _pmids_for_journal(journal, year=None, pmc_only=False):
    '''common function for all "pmids for journal name" endpoints below.'''
    qparams = { 'TA': journal, 'DP': year }
    pmids = collect_pmids_from_query('', pmc_only=pmc_only, debug=DEBUG, **qparams)
    return pmids

def _return_links_for_pmidlist(pmidlist):
    links = []
    for pmid in pmidlist:
        try:
            source = FindIt(pmid=pmid, debug=DEBUG, verify=False)
        except Exception as error:
            pass
        if source.url:
            links.append(source.url)
    return links

def _generate_link_csv(pmidlist):
    for pmid in pmidlist:
        try:
            source = FindIt(pmid=pmid, debug=DEBUG)
        except Exception as error:
            yield '%s,,%s\n' % (pmid, str(error))
        if source.url:
            yield '%s,%s,\n' % (pmid, source.url)
        else:
            yield '%s,,%s\n' % (pmid, source.reason)


@routes_v1.route('/v1/calculate/<journal>/<year>', methods=['GET'])
@routes_v1.route('/v1/calculate/<journal>', methods=['GET'])
@routes_v1.route('/v1/calculate/', methods=['POST'])
def calculate(journal=None, year=None):
    if request.method=='POST':
        journal = request.form.get('journal', None)
        year = request.form.get('year', None)
        log.debug('POST: calculate journal=%s, year=%s' % (journal, year))
        if year and journal:
            return redirect('/v1/calculate/%s/%s' % (journal, year), code=302)
        elif journal:
            return redirect('/v1/calculate/%s' % journal, code=302)
        else:
            return HTTP400("No journal name supplied")
    else:
        log.debug('GET: calculate journal=%s, year=%s' % (journal, year))

    outd = {'action': 'calculate', 'journal': journal, 'year': year}
    if journal:
        pmc_pmids = _pmids_for_journal(journal, year=year, pmc_only=True)
        all_pmids = _pmids_for_journal(journal, year=year, pmc_only=False)
        nonpmc_pmids = []

        for pmid in all_pmids:
            if pmid not in pmc_pmids:
                nonpmc_pmids.append(pmid)

        outd['PMC_count'] = len(pmc_pmids)
        outd['non_PMC_count'] = len(nonpmc_pmids)
        outd['all_pmids_count'] = len(all_pmids)

        links = _return_links_for_pmidlist(nonpmc_pmids)
        outd['num_nonpmc_links'] = len(links)

        return HTTP200(outd)

    else:
        return HTTP400("No journal supplied")


@routes_v1.route('/v1/all/<journal>', methods=['GET'])
@routes_v1.route('/v1/all/<journal>/<year>', methods=['GET'])
def get_all_pmids_for_journal(journal, year=None):
    if journal:
        all_pmids = _pmids_for_journal(journal, year=year, pmc_only=False)
        return HTTP200(all_pmids)
    else:
        return HTTP400("No journal supplied")

@routes_v1.route('/v1/pmc/<journal>', methods=['GET'])
@routes_v1.route('/v1/pmc/<journal>/<year>', methods=['GET'])
def get_pmc_pmids_for_journal(journal, year=None):
    if journal:
        pmc_pmids = _pmids_for_journal(journal, year=year, pmc_only=True)
        return HTTP200(pmc_pmids)
    else:
        return HTTP400("No journal supplied")

@routes_v1.route('/v1/nonpmc/<journal>', methods=['GET'])
@routes_v1.route('/v1/nonpmc/<journal>/<year>', methods=['GET'])
def get_nonpmc_pmids_for_journal(journal, year=None):
    if journal:
        pmc_pmids = _pmids_for_journal(journal, year=year, pmc_only=True)
        all_pmids = _pmids_for_journal(journal, year=year, pmc_only=False)
        nonpmc_pmids = []

        for pmid in all_pmids:
            if pmid not in pmc_pmids:
                nonpmc_pmids.append(pmid)
        return HTTP200(all_pmids)

    else:
        return HTTP400("No journal name supplied")

@routes_v1.route('/v1/links/<journal>/<year>', methods=['GET'])
@routes_v1.route('/v1/links/<journal>', methods=['GET'])
@routes_v1.route('/v1/links', methods=['POST'])
def get_links_for_journal(journal, year=None):
    if request.method=='POST':
        journal = request.form.get('journal', None)
        year = request.form.get('year', None)
        log.debug('POST: links for journal=%s, year=%s' % (journal, year))
        if year and journal:
            return redirect('/v1/links/%s/%s' % (journal, year), code=302)
        elif journal:
            return redirect('/v1/links/%s' % journal, code=302)
        else:
            return HTTP400("No journal name supplied")

    else:
        log.debug('GET: links for journal=%s, year=%s' % (journal, year))

    outd = {'action': 'links', 'journal': journal, 'year': year}
    if journal:
        pmc_pmids = _pmids_for_journal(journal, year=year, pmc_only=True)
        all_pmids = _pmids_for_journal(journal, year=year, pmc_only=False)
        nonpmc_pmids = []

        for pmid in all_pmids:
            if pmid not in pmc_pmids:
                nonpmc_pmids.append(pmid)

        outd['PMC_count'] = len(pmc_pmids)
        outd['non_PMC_count'] = len(nonpmc_pmids)
        outd['all_pmids_count'] = len(all_pmids)

        return Response(stream_with_context(_generate_link_csv(all_pmids)),
                        mimetype="application/json")

