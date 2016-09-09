# -*- coding: utf-8 -*-
# Copyright (c) 2014, 2015 Mitch Garnaat
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import kappa.event_source.base
import logging
import uuid

LOG = logging.getLogger(__name__)


class S3EventSource(kappa.event_source.base.EventSource):

    def __init__(self, context, config):
        super(S3EventSource, self).__init__(context, config)
        self._s3 = kappa.awsclient.create_client('s3', context.session)
        self._lambda = kappa.awsclient.create_client('lambda', context.session)

    def _make_notification_id(self, function_name):
        return 'Kappa-%s-notification' % function_name

    def _get_bucket_name(self):
        return self.arn.split(':')[-1]

    def _get_notification_spec(self, function):
            notification_spec = {
                'Id': self._make_notification_id(function.name),
                'Events': [e for e in self._config['events']],
                'LambdaFunctionArn': function.arn,
            }

            # Add S3 key filters
            if 'key_filters' in self._config:
                filters_spec = { 'Key' : { 'FilterRules' : [] } }
                for filter in self._config['key_filters']:
                    if 'type' in filter and 'value' in filter and filter['type'] in ('prefix', 'suffix'):
                        rule = { 'Name' : filter['type'].capitalize(), 'Value' : filter['value'] }
                        filters_spec['Key']['FilterRules'].append(rule)
                notification_spec['Filter'] = filters_spec

            return notification_spec

    def add(self, function):

        existingPermission={}
        try:
            response = self._lambda.call('get_policy',
                                     FunctionName=function.name)
            existingPermission = self.arn in str(response['Policy'])
        except Exception:
            LOG.debug('S3 event source permission not available')

        if not existingPermission:
            response = self._lambda.call('add_permission',
                                         FunctionName=function.name,
                                         StatementId=str(uuid.uuid4()),
                                         Action='lambda:InvokeFunction',
                                         Principal='s3.amazonaws.com',
                                         SourceArn=self.arn)
            LOG.debug(response)
        else:
            LOG.debug('S3 event source permission already exists')

        new_notification_spec = self._get_notification_spec(function)

        notification_spec_list = []
        try:
            response = self._s3.call(
                'get_bucket_notification_configuration',
                Bucket=self._get_bucket_name())
            LOG.debug(response)
            notification_spec_list = response['LambdaFunctionConfigurations']
        except Exception as exc:
            LOG.debug('Unable to get existing S3 event source notification configurations')

        if new_notification_spec not in notification_spec_list:
            notification_spec_list.append(new_notification_spec)
        else:       
            notification_spec_list=[]
            LOG.debug("S3 event source already exists")

        if notification_spec_list:

            notification_configuration = {
                'LambdaFunctionConfigurations': notification_spec_list
            }

            try:
                response = self._s3.call(
                    'put_bucket_notification_configuration',
                    Bucket=self._get_bucket_name(),
                    NotificationConfiguration=notification_configuration)
                LOG.debug(response)
            except Exception as exc:
                LOG.debug(exc.response)
                LOG.exception('Unable to add S3 event source')

    enable = add

    def update(self, function):
        self.add(function)

    def remove(self, function):

        notification_spec = self._get_notification_spec(function)

        LOG.debug('removing s3 notification')
        response = self._s3.call(
            'get_bucket_notification_configuration',
            Bucket=self._get_bucket_name())
        LOG.debug(response)

        if 'LambdaFunctionConfigurations' in response:
            notification_spec_list = response['LambdaFunctionConfigurations']

            if notification_spec in notification_spec_list:
                notification_spec_list.remove(notification_spec)
                response['LambdaFunctionConfigurations'] = notification_spec_list
                del response['ResponseMetadata']
                response = self._s3.call(
                    'put_bucket_notification_configuration',
                    Bucket=self._get_bucket_name(),
                    NotificationConfiguration=response)
                LOG.debug(response)

    disable = remove

    def status(self, function):
        LOG.debug('status for s3 notification for %s', function.name)

        notification_spec = self._get_notification_spec(function)

        response = self._s3.call(
            'get_bucket_notification_configuration',
            Bucket=self._get_bucket_name())
        LOG.debug(response)


        if 'LambdaFunctionConfigurations' not in response:
            return None
        
        notification_spec_list = response['LambdaFunctionConfigurations']
        if notification_spec not in notification_spec_list:
            return None
        
        return {
            'EventSourceArn': self.arn,
            'State': 'Enabled'
        }
