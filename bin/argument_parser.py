'''
 	Copyright (c) 2018, salesforce.com, inc.
	All rights reserved.
	SPDX-License-Identifier: BSD-3-Clause
	For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
'''

'''Argument parser for grover run.'''

import argparse


def parse_args():
    
    'Argument parser for grover'
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--access_token', help="Access token")
    parser.add_argument('-g', '--git_custom_url', help="Git custom url")
    parser.add_argument('-d', '--download_path', help="Download path for repos")
    parser.add_argument('-o', '--orgs', help="Org(s) list comma separated")
    parser.add_argument('-r', '--repos', help="Repo names optional")
    return parser.parse_args()
