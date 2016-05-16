import getpass

import requests

session = requests.Session()
session.auth = (input('github username: '), getpass.getpass('password: '))

def get(path, params={}):
    return session.get('https://api.github.com' + path, params=params).json()

def search_repositories(q, sort=None, per_page=None, page=None):
    params = {"q": q}
    if sort: params["sort"] = sort
    if per_page: params["per_page"] = per_page
    if page: params["page"] = page
    return get('/search/repositories', params)

def repository_contents(full_name, path='/'):
    return get('/repos/' + full_name + '/contents' + path)

def pull_request_comments(full_name, per_page=None, page=None):
    params = {}
    if per_page: params["per_page"] = per_page
    if page: params["page"] = page
    return get('/repos/' + full_name + '/pulls/comments', params)
