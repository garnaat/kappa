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

from kappa.stack import Stack
from tests.unit.mock_aws import get_aws

Config = {
    'template': 'roles.cf',
    'stack_name': 'FooBar',
    'exec_role': 'ExecRole',
    'invoke_role': 'InvokeRole'}


def path(filename):
    return os.path.join(os.path.dirname(__file__), 'data', filename)


class TestStack(unittest.TestCase):

    def setUp(self):
        self.aws_patch = mock.patch('kappa.aws.get_aws', get_aws)
        self.mock_aws = self.aws_patch.start()
        Config['template'] = path(Config['template'])

    def tearDown(self):
        self.aws_patch.stop()

    def test_properties(self):
        mock_context = mock.Mock()
        stack = Stack(mock_context, Config)
        self.assertEqual(stack.name, Config['stack_name'])
        self.assertEqual(stack.template_path, Config['template'])
        self.assertEqual(stack.exec_role, Config['exec_role'])
        self.assertEqual(stack.invoke_role, Config['invoke_role'])
        self.assertEqual(
            stack.invoke_role_arn,
            'arn:aws:iam::0123456789012:role/TestKinesis-InvokeRole-FOO')

    def test_exists(self):
        mock_context = mock.Mock()
        stack = Stack(mock_context, Config)
        self.assertTrue(stack.exists())

    def test_update(self):
        mock_context = mock.Mock()
        stack = Stack(mock_context, Config)
        stack.update()

    def test_delete(self):
        mock_context = mock.Mock()
        stack = Stack(mock_context, Config)
        stack.delete()
