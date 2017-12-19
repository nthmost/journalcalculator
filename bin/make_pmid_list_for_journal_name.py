import os, sys

from metapub import PubMedFetcher, FindIt

try:
    jtitle = sys.argv[1]
except IndexError:  
    print "supply journal name in quotation marks as argument to this script"
    sys.exit()

fetch = PubMedFetcher()

qparams = { 'jtitle': jtitle }
query = ''

pmid_file = open('PMID_lists/%s_all_pmids.txt' % jtitle.replace(' ', '_'), 'w')

retstart = 0
retmax = 500
while True:
    pmids = fetch.pmids_for_query(query, pmc_only=False, retstart=retstart, retmax=retmax, **qparams)
    if len(pmids) > 0:
        pmid_file.write('\n')
        pmid_file.write('\n'.join(pmids))
        retstart = retstart + retmax + 1
    else:
        break
    
pmid_file = open('PMID_lists/%s_pmc_only.txt' % jtitle.replace(' ', '_'), 'w')

retstart = 0
retmax = 500
while True:
    pmids = fetch.pmids_for_query(query, pmc_only=True, retstart=retstart, retmax=retmax, **qparams)
    if len(pmids) > 0:
        pmid_file.write('\n')
        pmid_file.write('\n'.join(pmids))
        retstart = retstart + retmax + 1
    else:
        break


