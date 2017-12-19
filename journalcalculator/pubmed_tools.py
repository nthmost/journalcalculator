from metapub import PubMedFetcher

fetch = PubMedFetcher()

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

