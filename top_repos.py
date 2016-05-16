import logging
import time

import github_api

logging.basicConfig(level=logging.DEBUG)


repos = []
for page in range(1, 100):
    logging.info('page %d', page)
    search = github_api.search_repositories('stars:>1000', per_page=100, page=page)
    if not search.get('items'): break
    repos += search['items']
    time.sleep(0.1)

logging.info('%d repos', len(repos))

for repo in repos:
    print('{stargazers_count}\t{full_name}'.format(**repo))
