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
import time

import botocore.session
from botocore.exceptions import ClientError

LOG = logging.getLogger(__name__)


class Kappa(object):

    completed_states = ('CREATE_COMPLETE', 'UPDATE_COMPLETE')

    def __init__(self, config):
        self.config = config
        self.session = botocore.session.get_session()
        self.session.profile = config['profile']
        self.region = config['region']

    def create_update_roles(self, stack_name, roles_path):
        LOG.debug('create_update_policies: stack_name=%s', stack_name)
        LOG.debug('create_update_policies: roles_path=%s', roles_path)
        cfn = self.session.create_client('cloudformation', self.region)
        # Does stack already exist?
        try:
            response = cfn.describe_stacks(StackName=stack_name)
            LOG.debug('Stack %s already exists', stack_name)
        except ClientError:
            LOG.debug('Stack %s does not exist', stack_name)
            response = None
        template_body = open(roles_path).read()
        if response:
            try:
                cfn.update_stack(
                    StackName=stack_name, TemplateBody=template_body,
                    Capabilities=['CAPABILITY_IAM'])
            except ClientError, e:
                LOG.debug(str(e))
        else:
            response = cfn.create_stack(
                StackName=stack_name, TemplateBody=template_body,
                Capabilities=['CAPABILITY_IAM'])
        done = False
        while not done:
            time.sleep(1)
            response = cfn.describe_stacks(StackName=stack_name)
            status = response['Stacks'][0]['StackStatus']
            LOG.debug('Stack status is: %s', status)
            if status in self.completed_states:
                done = True

    def get_role_arn(self, role_name):
        role_arn = None
        cfn = self.session.create_client('cloudformation', self.region)
        try:
            resources = cfn.list_stack_resources(
                StackName=self.config['cloudformation']['stack_name'])
        except Exception:
            LOG.exception('Unable to find role ARN: %s', role_name)
        for resource in resources['StackResourceSummaries']:
            if resource['LogicalResourceId'] == role_name:
                iam = self.session.create_client('iam')
                role = iam.get_role(RoleName=resource['PhysicalResourceId'])
                role_arn = role['Role']['Arn']
        LOG.debug('role_arn: %s', role_arn)
        return role_arn

    def delete_roles(self, stack_name):
        LOG.debug('delete_roles: stack_name=%s', stack_name)
        cfn = self.session.create_client('cloudformation', self.region)
        try:
            cfn.delete_stack(StackName=stack_name)
        except Exception:
            LOG.exception('Unable to delete stack: %s', stack_name)

    def _zip_lambda_dir(self, zipfile_name, lambda_dir):
        LOG.debug('_zip_lambda_dir: lambda_dir=%s', lambda_dir)
        LOG.debug('zipfile_name=%s', zipfile_name)
        relroot = os.path.abspath(os.path.join(lambda_dir, os.pardir))
        with zipfile.ZipFile(zipfile_name, 'w') as zf:
            for root, dirs, files in os.walk(lambda_dir):
                zf.write(root, os.path.relpath(root, relroot))
                for file in files:
                    filename = os.path.join(root, file)
                    if os.path.isfile(filename):
                        arcname = os.path.join(
                            os.path.relpath(root, relroot), file)
                        zf.write(filename, arcname)

    def _zip_lambda_file(self, zipfile_name, lambda_file):
        LOG.debug('_zip_lambda_file: lambda_file=%s', lambda_file)
        LOG.debug('zipfile_name=%s', zipfile_name)
        with zipfile.ZipFile(zipfile_name, 'w') as zf:
            zf.write(lambda_file)

    def zip_lambda_function(self, zipfile_name, lambda_fn):
        if os.path.isdir(lambda_fn):
            self._zip_lambda_dir(zipfile_name, lambda_fn)
        else:
            self._zip_lambda_file(zipfile_name, lambda_fn)

    def upload_lambda_function(self, zip_file):
        LOG.debug('uploading %s', zip_file)
        lambda_svc = self.session.create_client('lambda', self.region)
        with open(zip_file, 'rb') as fp:
            exec_role = self.get_role_arn(
                self.config['cloudformation']['exec_role'])
            try:
                response = lambda_svc.upload_function(
                    FunctionName=self.config['lambda']['name'],
                    FunctionZip=fp,
                    Runtime=self.config['lambda']['runtime'],
                    Role=exec_role,
                    Handler=self.config['lambda']['handler'],
                    Mode=self.config['lambda']['mode'],
                    Description=self.config['lambda']['description'],
                    Timeout=self.config['lambda']['timeout'],
                    MemorySize=self.config['lambda']['memory_size'])
                LOG.debug(response)
            except Exception:
                LOG.exception('Unable to upload zip file')

    def delete_lambda_function(self, function_name):
        LOG.debug('deleting function %s', function_name)
        lambda_svc = self.session.create_client('lambda', self.region)
        response = lambda_svc.delete_function(FunctionName=function_name)
        LOG.debug(response)
        return response

    def _invoke_asynch(self, data_file):
        LOG.debug('_invoke_async %s', data_file)
        with open(data_file) as fp:
            lambda_svc = self.session.create_client('lambda', self.region)
            response = lambda_svc.invoke_async(
                FunctionName=self.config['lambda']['name'],
                InvokeArgs=fp)
            LOG.debug(response)

    def _tail(self, function_name):
        LOG.debug('tailing function: %s', function_name)
        log_svc = self.session.create_client('logs', self.region)
        # kinda kludgy but can't find any way to get log group name
        log_group_name = '/aws/lambda/%s' % function_name
        latest_stream = None
        response = log_svc.describe_log_streams(logGroupName=log_group_name)
        # The streams are not ordered by time, hence this ugliness
        for stream in response['logStreams']:
            if not latest_stream:
                latest_stream = stream
            elif stream['lastEventTimestamp'] > latest_stream['lastEventTimestamp']:
                latest_stream = stream
        response = log_svc.get_log_events(
            logGroupName=log_group_name,
            logStreamName=latest_stream['logStreamName'])
        for log_event in response['events']:
            print(log_event['message'])

    def add_event_source(self):
        lambda_svc = self.session.create_client('lambda', self.region)
        try:
            invoke_role = self.get_role_arn(
                self.config['cloudformation']['invoke_role'])
            response = lambda_svc.add_event_source(
                FunctionName=self.config['lambda']['name'],
                Role=invoke_role,
                EventSource=self.config['lambda']['event_source'],
                BatchSize=self.config['lambda'].get('batch_size', 100))
            LOG.debug(response)
        except Exception:
            LOG.exception('Unable to add event source')

    def deploy(self):
        self.create_update_roles(
            self.config['cloudformation']['stack_name'],
            self.config['cloudformation']['template'])
        self.zip_lambda_function(
            self.config['lambda']['zipfile_name'],
            self.config['lambda']['path'])
        self.upload_lambda_function(self.config['lambda']['zipfile_name'])

    def test(self):
        self._invoke_asynch(self.config['lambda']['test_data'])

    def tail(self):
        self._tail(self.config['lambda']['name'])

    def delete(self):
        self.delete_roles(self.config['cloudformation']['stack_name'])
        self.delete_lambda_function(self.config['lambda']['name'])
