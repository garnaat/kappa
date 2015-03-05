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
    def mode(self):
        return self._config['mode']

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
    def arn(self):
        if self._arn is None:
            try:
                response = self._lambda_svc.get_function_configuration(
                    FunctionName=self.name)
                LOG.debug(response)
                self._arn = response['FunctionARN']
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

    def upload(self):
        LOG.debug('uploading %s', self.zipfile_name)
        self.zip_lambda_function(self.zipfile_name, self.path)
        with open(self.zipfile_name, 'rb') as fp:
            exec_role = self._context.exec_role_arn
            try:
                response = self._lambda_svc.upload_function(
                    FunctionName=self.name,
                    FunctionZip=fp,
                    Runtime=self.runtime,
                    Role=exec_role,
                    Handler=self.handler,
                    Mode=self.mode,
                    Description=self.description,
                    Timeout=self.timeout,
                    MemorySize=self.memory_size)
                LOG.debug(response)
            except Exception:
                LOG.exception('Unable to upload zip file')

    def delete(self):
        LOG.debug('deleting function %s', self.name)
        response = self._lambda_svc.delete_function(FunctionName=self.name)
        LOG.debug(response)
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

    def test(self):
        self.invoke_asynch(self.test_data)
