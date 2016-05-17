import logging
import re

import github_api

logging.basicConfig(level=logging.INFO)


ATTEMPTS = 5
TODO_RE = re.compile(r'\b(TODO|FIXME|XXX)\b', re.IGNORECASE)

def get_all_comments(repo):
    comments = []
    for page in range(1, 100):
        logging.debug('page %d', page)
        more = github_api.pull_request_comments(repo, per_page=100, page=page)
        if not more: break
        comments += more
    return comments

repos = []
with open('top_repos.txt') as f:
    for line in f:
        stars, repo = line.split()
        repos.append(repo)
logging.info('loaded %d repos', len(repos))

with open('comments.txt', 'w', encoding='utf-8') as f:
    for repo in repos:
        for i in range(ATTEMPTS):  # retry
            comments = get_all_comments(repo)
            try:
                for comment in comments:
                    comment['diff_line'] = comment['diff_hunk'].split('\n')[-1]
                break
            except TypeError as e:
                if i < ATTEMPTS - 1: logging.warning('retrying %s. invalid comment: %s', repo, comment)
                else: raise e

        todo_comments = [c for c in comments
                         if c['diff_line'].startswith('+') and TODO_RE.findall(c['diff_line'])]
        logging.info('%s has %d comments and %d todo comments', repo, len(comments), len(todo_comments))

        for c in todo_comments:
            f.write('\n'.join((c['html_url'], c['diff_line'], repr(c['body']), '', '')))
        f.flush()
