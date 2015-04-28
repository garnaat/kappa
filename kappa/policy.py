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

import kappa.aws

LOG = logging.getLogger(__name__)


class Policy(object):

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
    def description(self):
        return self._config.get('description', None)

    @property
    def document(self):
        return self._config.get('document', None)

    @property
    def path(self):
        return self._config.get('path', '/kappa/')

    @property
    def arn(self):
        if self._arn is None:
            policy = self.exists()
            if policy:
                self._arn = policy.get('Arn', None)
        return self._arn

    def _find_all_policies(self):
        # boto3 does not currently do pagination for ListPolicies
        # so we have to do it ourselves
        policies = []
        try:
            response = self._iam_svc.list_policies()
            policies += response['Policies']
            while response['IsTruncated']:
                LOG.debug('getting another page of policies')
                response = self._iam_svc.list_policies(
                    Marker=response['Marker'])
                policies += response['Policies']
        except Exception:
            LOG.exception('Error listing policies')
        return policies

    def exists(self):
        for policy in self._find_all_policies():
            if policy['PolicyName'] == self.name:
                return policy
        return None

    def create(self):
        LOG.debug('creating policy %s', self.name)
        policy = self.exists()
        if not policy and self.document:
            with open(self.document, 'rb') as fp:
                try:
                    response = self._iam_svc.create_policy(
                        Path=self.path, PolicyName=self.name,
                        PolicyDocument=fp.read(),
                        Description=self.description)
                    LOG.debug(response)
                except Exception:
                    LOG.exception('Error creating Policy')

    def delete(self):
        response = None
        # Only delete the policy if it has a document associated with it.
        # This indicates that it was a custom policy created by kappa.
        if self.arn and self.document:
            LOG.debug('deleting policy %s', self.name)
            response = self._iam_svc.delete_policy(PolicyArn=self.arn)
            LOG.debug(response)
        return response

    def status(self):
        LOG.debug('getting status for policy %s', self.name)
        return self.exists()
