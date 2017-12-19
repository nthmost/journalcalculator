from __future__ import print_function

import os, sys, logging

from metapub import PubMedFetcher, FindIt

logging.getLogger('eutils').setLevel(logging.INFO)

try:
    query = sys.argv[1]
except IndexError:  
    print("supply query in quotation marks as argument to this script.")
    sys.exit()

fetch = PubMedFetcher()

filename = 'PMID_lists/%s_all.txt' % query.replace(' ', '_')
pmid_file = open(filename, 'w')
print(filename)

retstart = 0
retmax = 500
while True:
    pmids = fetch.pmids_for_query(query, pmc_only=False, retstart=retstart, retmax=retmax)
    if len(pmids) > 0:
        pmid_file.write('\n')
        pmid_file.write('\n'.join(pmids))
        retstart = retstart + retmax + 1
    else:
        break

filename = 'PMID_lists/%s_pmc_only.txt' % query.replace(' ', '_')
pmid_file = open(filename, 'w')
print(filename)

retstart = 0
retmax = 500
while True:
    pmids = fetch.pmids_for_query(query, pmc_only=True, retstart=retstart, retmax=retmax)
    if len(pmids) > 0:
        pmid_file.write('\n')
        pmid_file.write('\n'.join(pmids))
        retstart = retstart + retmax + 1
    else:
        break


