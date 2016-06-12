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
import random
import string
from mock import Mock, call

from kappa.role import Role


def randomword(length):
    return ''.join(random.choice(string.printable) for i in range(length))


class TestRole(unittest.TestCase):

    def setUp(self):
        self.iam_client = Mock()
        policy = type('Policy', (object,), {
            'arn': None
        })
        self.context = type('Context', (object,), {
            'name': randomword(10),
            'environment': randomword(10),
            'policy': policy
        })
        self.role_record = {
            'RoleName': '%s_%s' % (self.context.name,
                                   self.context.environment),
            'Arn': randomword(10)
        }
        self.role = Role(self.context, None, iam_client=self.iam_client)

    def _expect_get_role(self):
        get_role_resp = {'Role': self.role_record}
        self.iam_client.configure_mock(**{
            'call.return_value': get_role_resp
        })
        return get_role_resp

    def test_delete_no_ops_if_role_not_found(self):
        self.iam_client.configure_mock(**{
            'call.return_value': None
        })
        self.assertEquals(None, self.role.delete())
        self.assertEquals(1, self.iam_client.call.call_count)

    def test_delete_when_role_exists(self):
        get_role_resp = self._expect_get_role()
        self.assertEquals(get_role_resp, self.role.delete())
        self.iam_client.call.assert_has_calls([call('get_role',
                                                    RoleName=self.role.name),
                                               call('delete_role',
                                                    RoleName=self.role.name)])

    def test_delete_policy_when_context_arn_exists(self):
        self.context.policy.arn = randomword(10)
        get_role_resp = self._expect_get_role()
        self.assertEquals(get_role_resp, self.role.delete())
        calls = [call('get_role',
                      RoleName=self.role.name),
                 call('detach_role_policy',
                      RoleName=self.role.name,
                      PolicyArn=self.context.policy.arn),
                 call('delete_role',
                      RoleName=self.role.name)]
        self.iam_client.call.assert_has_calls(calls)
