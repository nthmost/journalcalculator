import os, sys

from metapub import PubMedFetcher, FindIt

try:
    jtitle = sys.argv[1]
except IndexError:
    print "Supply journal title in quotation marks as argument to this script"
    sys.exit()

fetch = PubMedFetcher()

qparams = { 'jtitle': jtitle }
query = ''

out_fname = os.path.join('PMID_lists', jtitle.replace(' ', '_') + '.txt')

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

def write_pmids_to_file(pmids, filename):
    pmid_file = open(filename, 'w')
    pmid_file.write('\n')
    pmid_file.write('\n'.join(pmids))
    pmid_file.close()

pmc_pmids = collect_pmids_from_query('', pmc_only=True, **qparams)
all_pmids = collect_pmids_from_query('', pmc_only=False, **qparams)

write_pmids_to_file(pmc_pmids, 'PMID_lists/%s_pmconly_pmids.txt' % jtitle.replace(' ', '_'))
write_pmids_to_file(all_pmids, 'PMID_lists/%s_all_pmids.txt' % jtitle.replace(' ', '_'))

nonfree_pmids = []

for pmid in all_pmids:
    if pmid not in pmc_pmids:
        nonfree_pmids.append(pmid)

write_pmids_to_file(nonfree_pmids, 'PMID_lists/%s_nonpmc_pmids.txt' % jtitle.replace(' ', '_'))

print "Done: look at %s" % out_fname


