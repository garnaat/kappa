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
    def description(self):
        return self._config.get('description', None)

    @property
    def document(self):
        return self._config['document']

    @property
    def arn(self):
        if self._arn is None:
            policy = self.exists()
            if policy:
                self._arn = policy.get('Arn', None)
        return self._arn

    def exists(self):
        try:
            response = self._iam_svc.list_policies(PathPrefix=self.Path)
            LOG.debug(response)
            for policy in response['Policies']:
                if policy['PolicyName'] == self.name:
                    return policy
        except Exception:
            LOG.exception('Error listing policies')
        return None

    def create(self):
        LOG.debug('creating policy %s', self.name)
        policy = self.exists()
        if not policy:
            with open(self.document, 'rb') as fp:
                try:
                    response = self._iam_svc.create_policy(
                        Path=self.Path, PolicyName=self.name,
                        PolicyDocument=fp.read(),
                        Description=self.description)
                    LOG.debug(response)
                except Exception:
                    LOG.exception('Error creating Policy')

    def delete(self):
        response = None
        if self.arn:
            LOG.debug('deleting policy %s', self.name)
            response = self._iam_svc.delete_policy(PolicyArn=self.arn)
            LOG.debug(response)
        return response

    def status(self):
        LOG.debug('getting status for policy %s', self.name)
        return self.exists()
