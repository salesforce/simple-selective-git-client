#!/bin/sh

#
# Copyright (c) 2018, salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#

pip install virtualenv
virtualenv venv
. ./venv/bin/activate
pip install -r setup/requirements.txt
cd bin
