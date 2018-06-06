# -*- coding: utf-8 -*-
# Copyright (c) 2015 Mitch Garnaat http://garnaat.org/
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import unittest
import os
import shutil

import mock
import placebo

import kappa.context
import kappa.awsclient


class TestDeployUpdate(unittest.TestCase):

    def setUp(self):
        self.environ = {}
        self.environ_patch = mock.patch('os.environ', self.environ)
        self.environ_patch.start()
        self.prj_path = os.path.join(os.path.dirname(__file__), 'foobar')
        cache_file = os.path.join(self.prj_path, '.kappa')
        if os.path.exists(cache_file):
            shutil.rmtree(cache_file)
        self.data_path = os.path.join(os.path.dirname(__file__), 'responses')
        self.data_path = os.path.join(self.data_path, 'deploy_update')
        self.environ['AWS_ACCESS_KEY_ID'] = 'foo'
        self.environ['AWS_SECRET_ACCESS_KEY'] = 'bar'
        self.session = kappa.awsclient.create_session(None, 'us-east-1')

    def tearDown(self):
        pass

    def test_deploy_update_no_alias(self):
        pill = placebo.attach(self.session, self.data_path)
        pill.playback()
        os.chdir(self.prj_path)
        cfg_filepath = os.path.join(self.prj_path, 'kappa-new-alias.yml')
        cfg_fp = open(cfg_filepath)
        ctx = kappa.context.Context(cfg_fp, 'dev')
        ctx.deploy()

        cfg_fp = open(cfg_filepath)
        ctx = kappa.context.Context(cfg_fp, 'new-alias')
        ctx.deploy()
