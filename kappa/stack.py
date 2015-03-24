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
import time

import kappa.aws

LOG = logging.getLogger(__name__)


class Stack(object):

    completed_states = ('CREATE_COMPLETE', 'UPDATE_COMPLETE')
    failed_states = ('UPDATE_ROLLBACK_COMPLETE', 'ROLLBACK_COMPLETE')

    def __init__(self, context, config):
        self._context = context
        self._config = config
        aws = kappa.aws.get_aws(self._context)
        self._cfn = aws.create_client('cloudformation')
        self._iam = aws.create_client('iam')

    @property
    def name(self):
        return self._config['stack_name']

    @property
    def template_path(self):
        return self._config['template']

    @property
    def exec_role(self):
        return self._config['exec_role']

    @property
    def exec_role_arn(self):
        return self._get_role_arn(self.exec_role)

    @property
    def invoke_role(self):
        return self._config['invoke_role']

    @property
    def invoke_role_arn(self):
        return self._get_role_arn(self.invoke_role)

    def _get_role_arn(self, role_name):
        role_arn = None
        try:
            resources = self._cfn.list_stack_resources(
                StackName=self.name)
            LOG.debug(resources)
        except Exception:
            LOG.exception('Unable to find role ARN: %s', role_name)
        for resource in resources['StackResourceSummaries']:
            if resource['LogicalResourceId'] == role_name:
                role = self._iam.get_role(
                    RoleName=resource['PhysicalResourceId'])
                LOG.debug(role)
                role_arn = role['Role']['Arn']
        LOG.debug('role_arn: %s', role_arn)
        return role_arn

    def exists(self):
        """
        Does Cloudformation Stack already exist?
        """
        try:
            response = self._cfn.describe_stacks(StackName=self.name)
            LOG.debug('Stack %s exists', self.name)
        except Exception:
            LOG.debug('Stack %s does not exist', self.name)
            response = None
        return response

    def wait(self):
        done = False
        while not done:
            time.sleep(1)
            response = self._cfn.describe_stacks(StackName=self.name)
            LOG.debug(response)
            status = response['Stacks'][0]['StackStatus']
            LOG.debug('Stack status is: %s', status)
            if status in self.completed_states:
                done = True
            if status in self.failed_states:
                msg = 'Could not create stack %s: %s' % (self.name, status)
                raise ValueError(msg)

    def _create(self):
        LOG.debug('create_stack: stack_name=%s', self.name)
        template_body = open(self.template_path).read()
        try:
            response = self._cfn.create_stack(
                StackName=self.name, TemplateBody=template_body,
                Capabilities=['CAPABILITY_IAM'])
            LOG.debug(response)
        except Exception:
            LOG.exception('Unable to create stack')
        self.wait()

    def _update(self):
        LOG.debug('create_stack: stack_name=%s', self.name)
        template_body = open(self.template_path).read()
        try:
            response = self._cfn.update_stack(
                StackName=self.name, TemplateBody=template_body,
                Capabilities=['CAPABILITY_IAM'])
            LOG.debug(response)
        except Exception as e:
            if 'ValidationError' in str(e):
                LOG.info('No Updates Required')
            else:
                LOG.exception('Unable to update stack')
        self.wait()

    def update(self):
        if self.exists():
            self._update()
        else:
            self._create()

    def status(self):
        return self.exists()

    def delete(self):
        LOG.debug('delete_stack: stack_name=%s', self.name)
        try:
            response = self._cfn.delete_stack(StackName=self.name)
            LOG.debug(response)
        except Exception:
            LOG.exception('Unable to delete stack: %s', self.name)
