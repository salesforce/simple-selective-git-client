# A simple client for selective cloning of git repos 
Note: This has been tested/used with MacOS with python 2.7 for scanning orgs.

## Pre-requisities:
```
python 2.7 or python 3
pip
git access token - https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
```

## How to run?
```
1. cd <path_to_simple_git_client>/simple-selective-git-client

2. source setup/setupvenv.sh

3. You will land in bin directory. Here, run one of the commands below:

- To clone only selective repos when smaller number of repositories are supposed to be blacklisted by using blacklist.yaml

python run.py -a <access_token> -g "https://your_git_custom_url/api/<blah>" -d ~/Downloads/clonedRepos -o Org1

OR

- To clone only selective repos when a large number of repositories are supposed to be blacklisted

python run.py -a <access_token> -g "https://your_git_custom_url/api/<blah>" -d ~/Downloads/clonedRepos -o Org1 -r repo1,repo2


Example:  

## What does it do?
1. Gets repo list from org.
2. Clones repos. Skips those mentioned in blacklist.yaml file.
Note: Remove -d download folder if you need a fresh clone to happen, otherwise previously cloned repositories will be reused.

## What is blacklist.yaml file?
It has org, repositories names which need to be skipped.
```
Format:
```
Org1:
	- Repo1
	- Repo2
Org2:
	- Repo3
	- Repo4
```

## References
https://pygithub.readthedocs.io/en/latest/apis.html <br>
https://gitpython.readthedocs.io/en/stable/reference.html
