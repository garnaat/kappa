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

import logging

from botocore.exceptions import ClientError

import kappa.aws

LOG = logging.getLogger(__name__)


AssumeRolePolicyDocument = """{
    "Version" : "2012-10-17",
    "Statement": [ {
        "Effect": "Allow",
        "Principal": {
            "Service": [ "lambda.amazonaws.com" ]
        },
        "Action": [ "sts:AssumeRole" ]
    } ]
}"""


class Role(object):

    Path = '/kappa/'

    def __init__(self, context, config):
        self._context = context
        self._config = config
        aws = kappa.aws.get_aws(context)
        self._iam_svc = aws.create_client('iam')
        self._arn = None

    @property
    def name(self):
        return self._config['name']

    @property
    def arn(self):
        if self._arn is None:
            try:
                response = self._iam_svc.get_role(
                    RoleName=self.name)
                LOG.debug(response)
                self._arn = response['Role']['Arn']
            except Exception:
                LOG.debug('Unable to find ARN for role: %s', self.name)
        return self._arn

    def exists(self):
        try:
            response = self._iam_svc.list_roles(PathPrefix=self.Path)
            LOG.debug(response)
            for role in response['Roles']:
                if role['RoleName'] == self.name:
                    return role
        except Exception:
            LOG.exception('Error listing roles')
        return None

    def create(self):
        LOG.debug('creating role %s', self.name)
        role = self.exists()
        if not role:
            try:
                response = self._iam_svc.create_role(
                    Path=self.Path, RoleName=self.name,
                    AssumeRolePolicyDocument=AssumeRolePolicyDocument)
                LOG.debug(response)
                if self._context.policy:
                    LOG.debug('attaching policy %s', self._context.policy.arn)
                    response = self._iam_svc.attach_role_policy(
                        RoleName=self.name,
                        PolicyArn=self._context.policy.arn)
                    LOG.debug(response)
            except ClientError:
                LOG.exception('Error creating Role')

    def delete(self):
        response = None
        LOG.debug('deleting role %s', self.name)
        try:
            LOG.debug('First detach the policy from the role')
            policy_arn = self._context.policy.arn
            if policy_arn:
                response = self._iam_svc.detach_role_policy(
                    RoleName=self.name, PolicyArn=policy_arn)
                LOG.debug(response)
            response = self._iam_svc.delete_role(RoleName=self.name)
            LOG.debug(response)
        except ClientError:
            LOG.exception('role %s not found', self.name)
        return response

    def status(self):
        LOG.debug('getting status for role %s', self.name)
        try:
            response = self._iam_svc.get_role(RoleName=self.name)
            LOG.debug(response)
        except ClientError:
            LOG.debug('role %s not found', self.name)
            response = None
        return response
