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

from botocore.exceptions import ClientError

import kappa.aws

LOG = logging.getLogger(__name__)


class EventSource(object):

    def __init__(self, context, config):
        self._context = context
        self._config = config

    @property
    def arn(self):
        return self._config['arn']

    @property
    def batch_size(self):
        return self._config.get('batch_size', 100)


class KinesisEventSource(EventSource):

    def __init__(self, context, config):
        super(KinesisEventSource, self).__init__(context, config)
        aws = kappa.aws.get_aws(context)
        self._lambda = aws.create_client('lambda')

    def _get_uuid(self, function):
        uuid = None
        response = self._lambda.list_event_sources(
            FunctionName=function.name,
            EventSourceArn=self.arn)
        LOG.debug(response)
        if len(response['EventSources']) > 0:
            uuid = response['EventSources'][0]['UUID']
        return uuid

    def add(self, function):
        try:
            response = self._lambda.add_event_source(
                FunctionName=function.name,
                Role=self._context.invoke_role_arn,
                EventSource=self.arn,
                BatchSize=self.batch_size)
            LOG.debug(response)
        except Exception:
            LOG.exception('Unable to add Kinesis event source')

    def remove(self, function):
        response = None
        uuid = self._get_uuid(function)
        if uuid:
            response = self._lambda.remove_event_source(
                UUID=uuid)
            LOG.debug(response)
        return response

    def status(self, function):
        LOG.debug('getting status for event source %s', self.arn)
        try:
            response = self._lambda.get_event_source(
                UUID=self._get_uuid(function))
            LOG.debug(response)
        except ClientError:
            LOG.debug('event source %s does not exist', self.arn)
            response = None
        return response


class S3EventSource(EventSource):

    def __init__(self, context, config):
        super(S3EventSource, self).__init__(context, config)
        aws = kappa.aws.get_aws(context)
        self._s3 = aws.create_client('s3')

    def _make_notification_id(self, function_name):
        return 'Kappa-%s-notification' % function_name

    def _get_bucket_name(self):
        return self.arn.split(':')[-1]

    def add(self, function):
        notification_spec = {
            'CloudFunctionConfiguration': {
                'Id': self._make_notification_id(function.name),
                'Events': [e for e in self._config['events']],
                'CloudFunction': function.arn,
                'InvocationRole': self._context.invoke_role_arn}}
        try:
            response = self._s3.put_bucket_notification(
                Bucket=self._get_bucket_name(),
                NotificationConfiguration=notification_spec)
            LOG.debug(response)
        except Exception:
            LOG.exception('Unable to add S3 event source')

    def remove(self, function):
        LOG.debug('removing s3 notification')
        response = self._s3.get_bucket_notification(
            Bucket=self._get_bucket_name())
        LOG.debug(response)
        if 'CloudFunctionConfiguration' in response:
            fn_arn = response['CloudFunctionConfiguration']['CloudFunction']
            if fn_arn == function.arn:
                del response['CloudFunctionConfiguration']
                response = self._s3.put_bucket_notification(
                    Bucket=self._get_bucket_name(),
                    NotificationConfiguration=response)
                LOG.debug(response)

    def status(self, function):
        LOG.debug('status for s3 notification for %s', function.name)
        response = self._s3.get_bucket_notification(
            Bucket=self._get_bucket_name())
        LOG.debug(response)
        if 'CloudFunctionConfiguration' not in response:
            response = None
        return response
