'''
    Copyright (c) 2018, salesforce.com, inc.
    All rights reserved.
    SPDX-License-Identifier: BSD-3-Clause
    For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
'''

import argument_parser
import logging
import time

from github import Github

logging.root.handlers = []
logging.basicConfig(format='%(message)s', level=logging.INFO,
                    filename='/tmp/flex-git-client-output-' + str(time.time()) + '.log')

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(message)s')

console.setFormatter(formatter)
logging.getLogger().addHandler(console)


def clone_repo(g, url, repo_download_location):
    ''' Clones repo.'''

    import git
    git.Repo.clone_from(url, repo_download_location)


def get_repos_by_name(git_custom_url, access_token, orgs_list, repo_names):
    ''' Get git handle for Github Enterprise with custom hostname. '''

    g = get_git_handle(git_custom_url, access_token)
    org_name = orgs_list[0]
    git_repos = {}
    git_repos[org_name] = []
    for repo_name in repo_names:
        git_repo = g.get_organization(org_name).get_repo(repo_name)
        git_repos[org_name].append(git_repo)

    logging.info(git_repos)

    return g, git_repos


def get_git_handle(git_custom_url, access_token):
    ''' Get git handle. '''

    g = Github(base_url=git_custom_url,
               login_or_token=access_token, verify=False)
    return g


def get_repos_from_git(git_custom_url, access_token, orgs_list):
    ''' Github Enterprise with custom hostname. '''

    g = get_git_handle(git_custom_url, access_token)

    git_repos = {}
    for org_name in orgs_list:
        git_org = g.get_organization(org_name)
        git_repos[org_name] = []
        index_of_page = 0
        while len(git_org.get_repos().get_page(index_of_page)) > 0:
            git_repos[org_name] += (git_org.get_repos().get_page(index_of_page))
            index_of_page = index_of_page + 1
            logging.info("Finished reading page %d", index_of_page)
        logging.info(git_repos)

    return g, git_repos


def flatten(repos):
    ''' Flatten as org.repo. '''

    flat_skip_repos = []
    for each_org in repos:
        flat_skip_repos += ([str(each_org) + "." + str(each_repo)
                             for each_repo in repos[each_org]])

    return flat_skip_repos


if __name__ == '__main__':

    ''' Parse input arguments for every git org, or for input git repos
    .'''

    g = None  # Git handle

    # Parse args
    args = argument_parser.parse_args()

    access_token = args.access_token or None
    download_path = args.download_path or None
    git_custom_url = args.git_custom_url or None
    repos = args.repos or None
    orgs = args.orgs or None

    if None in (access_token, download_path, orgs, git_custom_url):
        logging.error(
            "Usage: Incorrect inputs, Required: access_token download_path <orgs_list_comma_separated> git_custom_url")
        exit(1)

    repos = args.repos.split(",") if args.repos else None
    orgs = args.orgs.split(",") or None
    # Read YAML file for backlisted repos
    import yaml
    import os
    with open("../config/blacklist.yaml", 'r') as stream:
        skip_repos = yaml.load(stream)
    logging.info("Loaded blacklisted repos %s " % str(skip_repos))

    flat_skip_repos = []
    if skip_repos:
        flat_skip_repos = flatten(skip_repos)

    logging.info("Flat blacklisted repos %s " % str(flat_skip_repos))

    if not repos:
        g, git_repos = get_repos_from_git(git_custom_url, access_token, orgs)
    elif len(orgs) == 1 and repos:
        g, git_repos = get_repos_by_name(git_custom_url, access_token, orgs, repos)
    else:
        logging.error("Please pass 1 org and multiple repos!")
        exit(1)

    download_path_prefix = download_path + "/"
    if not os.path.exists(download_path_prefix):
        os.mkdir(download_path_prefix)

    ''' For every org, create a org directory,
        for all repos, create repo directories inside it, clone them
    '''

    for each_org in git_repos:

        # org directory creation
        download_path_prefix = download_path + \
            "/" + str(each_org).strip() + "/"
        if not os.path.exists(download_path_prefix):
            os.mkdir(download_path_prefix)

        # for every org, clone repos
        for each_repo in git_repos[each_org]:
            cur_repo = each_org + "." + each_repo.name
            if cur_repo in flat_skip_repos:
                logging.info("Current repo to skip %s " % str(cur_repo))
            else:
                logging.info("Working on %s" % cur_repo)

                clone_url = str(g.get_organization(
                    each_org).get_repo(each_repo.name).ssh_url)
                repo_path = download_path_prefix + each_repo.name

                if not os.path.exists(repo_path):
                    clone_repo(g, clone_url, repo_path)

    logging.info("All done")
