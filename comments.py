import logging
import re

import github_api

logging.basicConfig(level=logging.INFO)


TODO_RE = re.compile(r'\b(TODO|FIXME|XXX)\b', re.IGNORECASE)

def get_all_comments(repo):
    comments = []
    for page in range(1, 100):
        logging.debug('page %d', page)
        more = github_api.pull_request_comments(repo, per_page=100, page=page)
        if not more: break
        comments += more
    return comments

def save_comments(repo, comments):
    path = 'comments/' + repo.replace('/', '-')
    with open(path, 'w', encoding='utf-8') as f:
        for c in comments:
            f.write('{}\n{}\n{}\n\n'.format(c['url'], repr(c['diff_line']), repr(c['body'])))

repos = []
with open('top_repos.txt') as f:
    for line in f:
        stars, repo = line.split()
        repos.append(repo)
logging.info('loaded %d repos', len(repos))

for repo in repos:
    n = 0
    comments = get_all_comments(repo)
    for comment in comments:
        comment['diff_line'] = comment['diff_hunk'].split('\n')[-1]
    todo_comments = [c for c in comments
                     if c['diff_line'].startswith('+') and TODO_RE.findall(c['diff_line'])]
    logging.info('%s has %d comments and %d todo comments', repo, len(comments), len(todo_comments))
    if todo_comments: save_comments(repo, todo_comments)
