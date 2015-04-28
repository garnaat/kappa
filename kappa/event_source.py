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
    def starting_position(self):
        return self._config.get('starting_position', 'TRIM_HORIZON')

    @property
    def batch_size(self):
        return self._config.get('batch_size', 100)

    @property
    def enabled(self):
        return self._config.get('enabled', True)


class KinesisEventSource(EventSource):

    def __init__(self, context, config):
        super(KinesisEventSource, self).__init__(context, config)
        aws = kappa.aws.get_aws(context)
        self._lambda = aws.create_client('lambda')

    def _get_uuid(self, function):
        uuid = None
        response = self._lambda.list_event_source_mappings(
            FunctionName=function.name,
            EventSourceArn=self.arn)
        LOG.debug(response)
        if len(response['EventSourceMappings']) > 0:
            uuid = response['EventSourceMappings'][0]['UUID']
        return uuid

    def add(self, function):
        try:
            response = self._lambda.create_event_source_mapping(
                FunctionName=function.name,
                EventSourceArn=self.arn,
                BatchSize=self.batch_size,
                StartingPosition=self.starting_position,
                Enabled=self.enabled
            )
            LOG.debug(response)
        except Exception:
            LOG.exception('Unable to add event source')

    def update(self, function):
        response = None
        uuid = self._get_uuid(function)
        if uuid:
            try:
                response = self._lambda.update_event_source_mapping(
                    BatchSize=self.batch_size,
                    Enabled=self.enabled,
                    FunctionName=function.arn)
                LOG.debug(response)
            except Exception:
                LOG.exception('Unable to update event source')

    def remove(self, function):
        response = None
        uuid = self._get_uuid(function)
        if uuid:
            response = self._lambda.delete_event_source_mapping(
                UUID=uuid)
            LOG.debug(response)
        return response

    def status(self, function):
        response = None
        LOG.debug('getting status for event source %s', self.arn)
        uuid = self._get_uuid(function)
        if uuid:
            try:
                response = self._lambda.get_event_source_mapping(
                    UUID=self._get_uuid(function))
                LOG.debug(response)
            except ClientError:
                LOG.debug('event source %s does not exist', self.arn)
                response = None
        else:
            LOG.debug('No UUID for event source %s', self.arn)
        return response


class DynamoDBStreamEventSource(KinesisEventSource):

    pass


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


class SNSEventSource(EventSource):

    def __init__(self, context, config):
        super(SNSEventSource, self).__init__(context, config)
        aws = kappa.aws.get_aws(context)
        self._sns = aws.create_client('sns')

    def _make_notification_id(self, function_name):
        return 'Kappa-%s-notification' % function_name

    def exists(self, function):
        try:
            response = self._sns.list_subscriptions_by_topic(
                TopicArn=self.arn)
            LOG.debug(response)
            for subscription in response['Subscriptions']:
                if subscription['Endpoint'] == function.arn:
                    return subscription
            return None
        except Exception:
            LOG.exception('Unable to find event source %s', self.arn)

    def add(self, function):
        try:
            response = self._sns.subscribe(
                TopicArn=self.arn, Protocol='lambda',
                Endpoint=function.arn)
            LOG.debug(response)
        except Exception:
            LOG.exception('Unable to add SNS event source')

    def remove(self, function):
        LOG.debug('removing SNS event source')
        try:
            subscription = self.exists(function)
            if subscription:
                response = self._sns.unsubscribe(
                    SubscriptionArn=subscription['SubscriptionArn'])
                LOG.debug(response)
        except Exception:
            LOG.exception('Unable to remove event source %s', self.arn)

    def status(self, function):
        LOG.debug('status for SNS notification for %s', function.name)
        return self.exists(function)
