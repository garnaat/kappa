# Copyright (c) 2014 Mitch Garnaat http://garnaat.org/
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

from kappa.log import Log
from mock_aws import get_aws


class TestLog(unittest.TestCase):

    def setUp(self):
        self.aws_patch = mock.patch('kappa.aws.get_aws', get_aws)
        self.mock_aws = self.aws_patch.start()

    def tearDown(self):
        self.aws_patch.stop()

    def test_streams(self):
        mock_context = mock.Mock()
        log = Log(mock_context, 'foo/bar')
        streams = log.streams()
        self.assertEqual(len(streams), 6)

    def test_tail(self):
        mock_context = mock.Mock()
        log = Log(mock_context, 'foo/bar')
        events = log.tail()
        self.assertEqual(len(events), 6)
        self.assertEqual(events[0]['ingestionTime'], 1420569036909)
        self.assertIn('RequestId: 23007242-95d2-11e4-a10e-7b2ab60a7770',
                      events[-1]['message'])
