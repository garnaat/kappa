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
import os
import zipfile

from botocore.exceptions import ClientError

import kappa.aws
import kappa.log

LOG = logging.getLogger(__name__)


class Function(object):

    def __init__(self, context, config):
        self._context = context
        self._config = config
        aws = kappa.aws.get_aws(context)
        self._lambda_svc = aws.create_client('lambda')
        self._arn = None
        self._log = None

    @property
    def name(self):
        return self._config['name']

    @property
    def runtime(self):
        return self._config['runtime']

    @property
    def handler(self):
        return self._config['handler']

    @property
    def description(self):
        return self._config['description']

    @property
    def timeout(self):
        return self._config['timeout']

    @property
    def memory_size(self):
        return self._config['memory_size']

    @property
    def zipfile_name(self):
        return self._config['zipfile_name']

    @property
    def path(self):
        return self._config['path']

    @property
    def test_data(self):
        return self._config['test_data']

    @property
    def permissions(self):
        return self._config.get('permissions', list())

    @property
    def arn(self):
        if self._arn is None:
            try:
                response = self._lambda_svc.get_function(
                    FunctionName=self.name)
                LOG.debug(response)
                self._arn = response['Configuration']['FunctionArn']
            except Exception:
                LOG.debug('Unable to find ARN for function: %s', self.name)
        return self._arn

    @property
    def log(self):
        if self._log is None:
            log_group_name = '/aws/lambda/%s' % self.name
            self._log = kappa.log.Log(self._context, log_group_name)
        return self._log

    def tail(self):
        LOG.debug('tailing function: %s', self.name)
        return self.log.tail()

    def _zip_lambda_dir(self, zipfile_name, lambda_dir):
        LOG.debug('_zip_lambda_dir: lambda_dir=%s', lambda_dir)
        LOG.debug('zipfile_name=%s', zipfile_name)
        relroot = os.path.abspath(lambda_dir)
        with zipfile.ZipFile(zipfile_name, 'w',
                             compression=zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(lambda_dir):
                zf.write(root, os.path.relpath(root, relroot))
                for filename in files:
                    filepath = os.path.join(root, filename)
                    if os.path.isfile(filepath):
                        arcname = os.path.join(
                            os.path.relpath(root, relroot), filename)
                        zf.write(filepath, arcname)

    def _zip_lambda_file(self, zipfile_name, lambda_file):
        LOG.debug('_zip_lambda_file: lambda_file=%s', lambda_file)
        LOG.debug('zipfile_name=%s', zipfile_name)
        with zipfile.ZipFile(zipfile_name, 'w',
                             compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(lambda_file)

    def zip_lambda_function(self, zipfile_name, lambda_fn):
        if os.path.isdir(lambda_fn):
            self._zip_lambda_dir(zipfile_name, lambda_fn)
        else:
            self._zip_lambda_file(zipfile_name, lambda_fn)

    def add_permissions(self):
        for permission in self.permissions:
            try:
                kwargs = {
                    'FunctionName': self.name,
                    'StatementId': permission['statement_id'],
                    'Action': permission['action'],
                    'Principal': permission['principal']}
                source_arn = permission.get('source_arn', None)
                if source_arn:
                    kwargs['SourceArn'] = source_arn
                source_account = permission.get('source_account', None)
                if source_account:
                    kwargs['SourceAccount'] = source_account
                response = self._lambda_svc.add_permission(**kwargs)
                LOG.debug(response)
            except Exception:
                LOG.exception('Unable to add permission')

    def create(self):
        LOG.debug('creating %s', self.zipfile_name)
        self.zip_lambda_function(self.zipfile_name, self.path)
        with open(self.zipfile_name, 'rb') as fp:
            exec_role = self._context.exec_role_arn
            LOG.debug('exec_role=%s', exec_role)
            try:
                zipdata = fp.read()
                response = self._lambda_svc.create_function(
                    FunctionName=self.name,
                    Code={'ZipFile': zipdata},
                    Runtime=self.runtime,
                    Role=exec_role,
                    Handler=self.handler,
                    Description=self.description,
                    Timeout=self.timeout,
                    MemorySize=self.memory_size)
                LOG.debug(response)
            except Exception:
                LOG.exception('Unable to upload zip file')
        self.add_permissions()

    def update(self):
        LOG.debug('updating %s', self.zipfile_name)
        self.zip_lambda_function(self.zipfile_name, self.path)
        with open(self.zipfile_name, 'rb') as fp:
            try:
                zipdata = fp.read()
                response = self._lambda_svc.update_function_code(
                    FunctionName=self.name,
                    ZipFile=zipdata)
                LOG.debug(response)
            except Exception:
                LOG.exception('Unable to update zip file')

    def delete(self):
        LOG.debug('deleting function %s', self.name)
        response = None
        try:
            response = self._lambda_svc.delete_function(FunctionName=self.name)
            LOG.debug(response)
        except ClientError:
            LOG.debug('function %s: not found', self.name)
        return response

    def status(self):
        LOG.debug('getting status for function %s', self.name)
        try:
            response = self._lambda_svc.get_function(
                FunctionName=self.name)
            LOG.debug(response)
        except ClientError:
            LOG.debug('function %s not found', self.name)
            response = None
        return response

    def invoke_asynch(self, data_file):
        LOG.debug('_invoke_async %s', data_file)
        with open(data_file) as fp:
            response = self._lambda_svc.invoke_async(
                FunctionName=self.name,
                InvokeArgs=fp)
            LOG.debug(response)

    def _invoke(self, test_data, invocation_type):
        if test_data is None:
            test_data = self.test_data
        LOG.debug('invoke %s', test_data)
        with open(test_data) as fp:
            response = self._lambda_svc.invoke(
                FunctionName=self.name,
                InvocationType=invocation_type,
                LogType='Tail',
                Payload=fp.read())
        LOG.debug(response)
        return response

    def invoke(self, test_data=None):
        return self._invoke(test_data, 'RequestResponse')

    def invoke_async(self, test_data=None):
        return self._invoke(test_data, 'Event')

    def dryrun(self, test_data=None):
        return self._invoke(test_data, 'DryRun')
