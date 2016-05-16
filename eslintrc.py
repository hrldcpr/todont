import logging

import requests

import github_api

logging.basicConfig(level=logging.INFO)


session = requests.Session()
def download(repo, name, url):
    text = session.get(url).text
    path = 'eslintrc/{}-{}'.format(repo.replace('/', '-'), name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


repos = []
with open('top_repos.txt') as f:
    for line in f:
        stars, repo = line.split()
        repos.append(repo)
logging.info('loaded %d repos', len(repos))

for repo in repos:
    n = 0
    contents = github_api.repository_contents(repo)
    for f in contents:
        if 'eslintrc' in f['name'].lower():
            if f['type'] == 'file':
                n += 1
                download(repo, f['name'], f['download_url'])
            else:
                logging.warn('%s has weird eslintrc directory %s', repo, f['name'])
    if n:
        logging.info('%s has %d eslintrc files', repo, n)
