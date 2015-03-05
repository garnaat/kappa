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

import logging

LOG = logging.getLogger(__name__)

import kappa.aws


class Log(object):

    def __init__(self, context, log_group_name):
        self._context = context
        self.log_group_name = log_group_name
        aws = kappa.aws.get_aws(self._context)
        self._log_svc = aws.create_client('logs')

    def _check_for_log_group(self):
        LOG.debug('checking for log group')
        response = self._log_svc.describe_log_groups()
        log_group_names = [lg['logGroupName'] for lg in response['logGroups']]
        return self.log_group_name in log_group_names

    def streams(self):
        LOG.debug('getting streams for log group: %s', self.log_group_name)
        if not self._check_for_log_group():
            LOG.info(
                'log group %s has not been created yet', self.log_group_name)
            return []
        response = self._log_svc.describe_log_streams(
            logGroupName=self.log_group_name)
        LOG.debug(response)
        return response['logStreams']

    def tail(self):
        LOG.debug('tailing log group: %s', self.log_group_name)
        if not self._check_for_log_group():
            LOG.info(
                'log group %s has not been created yet', self.log_group_name)
            return []
        latest_stream = None
        streams = self.streams()
        for stream in streams:
            if not latest_stream:
                latest_stream = stream
            elif stream['lastEventTimestamp'] > latest_stream['lastEventTimestamp']:
                latest_stream = stream
        response = self._log_svc.get_log_events(
            logGroupName=self.log_group_name,
            logStreamName=latest_stream['logStreamName'])
        LOG.debug(response)
        return response['events']
