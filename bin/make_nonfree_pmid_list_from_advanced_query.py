import os, sys

from metapub import PubMedFetcher, FindIt

try:
    query = sys.argv[1]
except IndexError:
    print "Supply advanced query surrounded by quotation marks."
    sys.exit()

fetch = PubMedFetcher()

out_fname = os.path.join('PMID_lists', query.replace(' ', '_') + '_NONFREE.txt')

def collect_pmids_from_query(query, pmc_only, **kwargs):
    retstart = 0
    retmax = 500
    pmid_total = [] 
    while True:
        pmids = fetch.pmids_for_query(query, pmc_only=pmc_only, retstart=retstart, retmax=retmax, **kwargs)
        if len(pmids) > 0:
            pmid_total += pmids
            retstart = retstart + retmax + 1
        else:
            return pmid_total

pmc_pmids = collect_pmids_from_query(query, pmc_only=True)  #, **qparams)
all_pmids = collect_pmids_from_query(query, pmc_only=False)  #, **qparams)

nonfree_pmids = []

for pmid in all_pmids:
    if pmid not in pmc_pmids:
        nonfree_pmids.append(pmid)

open(out_fname, 'w').write('\n'.join(nonfree_pmids))
print "Done: look at %s" % out_fname

