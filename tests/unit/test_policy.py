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

import mock

from kappa.policy import Policy
from tests.unit.mock_aws import get_aws

Config1 = {
    'name': 'FooPolicy',
    'description': 'This is the Foo policy',
    'document': 'FooPolicy.json'}

Config2 = {
    'name': 'BazPolicy',
    'description': 'This is the Baz policy',
    'document': 'BazPolicy.json'}


def path(filename):
    return os.path.join(os.path.dirname(__file__), 'data', filename)


class TestPolicy(unittest.TestCase):

    def setUp(self):
        self.aws_patch = mock.patch('kappa.aws.get_aws', get_aws)
        self.mock_aws = self.aws_patch.start()
        Config1['document'] = path(Config1['document'])
        Config2['document'] = path(Config2['document'])

    def tearDown(self):
        self.aws_patch.stop()

    def test_properties(self):
        mock_context = mock.Mock()
        policy = Policy(mock_context, Config1)
        self.assertEqual(policy.name, Config1['name'])
        self.assertEqual(policy.document, Config1['document'])
        self.assertEqual(policy.description, Config1['description'])

    def test_exists(self):
        mock_context = mock.Mock()
        policy = Policy(mock_context, Config1)
        self.assertTrue(policy.exists())

    def test_not_exists(self):
        mock_context = mock.Mock()
        policy = Policy(mock_context, Config2)
        self.assertFalse(policy.exists())

    def test_create(self):
        mock_context = mock.Mock()
        policy = Policy(mock_context, Config2)
        policy.create()

    def test_delete(self):
        mock_context = mock.Mock()
        policy = Policy(mock_context, Config1)
        policy.delete()
