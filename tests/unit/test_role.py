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

import mock

from kappa.role import Role
from tests.unit.mock_aws import get_aws

Config1 = {'name': 'FooRole'}

Config2 = {'name': 'BazRole'}


class TestRole(unittest.TestCase):

    def setUp(self):
        self.aws_patch = mock.patch('kappa.aws.get_aws', get_aws)
        self.mock_aws = self.aws_patch.start()

    def tearDown(self):
        self.aws_patch.stop()

    def test_properties(self):
        mock_context = mock.Mock()
        role = Role(mock_context, Config1)
        self.assertEqual(role.name, Config1['name'])

    def test_exists(self):
        mock_context = mock.Mock()
        role = Role(mock_context, Config1)
        self.assertTrue(role.exists())

    def test_not_exists(self):
        mock_context = mock.Mock()
        role = Role(mock_context, Config2)
        self.assertFalse(role.exists())

    def test_create(self):
        mock_context = mock.Mock()
        role = Role(mock_context, Config2)
        role.create()

    def test_delete(self):
        mock_context = mock.Mock()
        role = Role(mock_context, Config1)
        role.delete()
