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
import yaml
import time

import kappa.function
import kappa.event_source
import kappa.policy
import kappa.role

LOG = logging.getLogger(__name__)

DebugFmtString = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
InfoFmtString = '\t%(message)s'


class Context(object):

    def __init__(self, config_file, debug=False):
        if debug:
            self.set_logger('kappa', logging.DEBUG)
        else:
            self.set_logger('kappa', logging.INFO)
        self.config = yaml.load(config_file)
        if 'policy' in self.config.get('iam', ''):
            self.policy = kappa.policy.Policy(
                self, self.config['iam']['policy'])
        else:
            self.policy = None
        if 'role' in self.config.get('iam', ''):
            self.role = kappa.role.Role(
                self, self.config['iam']['role'])
        else:
            self.role = None
        self.function = kappa.function.Function(
            self, self.config['lambda'])
        self.event_sources = []
        self._create_event_sources()

    @property
    def profile(self):
        return self.config.get('profile', None)

    @property
    def region(self):
        return self.config.get('region', None)

    @property
    def lambda_config(self):
        return self.config.get('lambda', None)

    @property
    def exec_role_arn(self):
        return self.role.arn

    def debug(self):
        self.set_logger('kappa', logging.DEBUG)

    def set_logger(self, logger_name, level=logging.INFO):
        """
        Convenience function to quickly configure full debug output
        to go to the console.
        """
        log = logging.getLogger(logger_name)
        log.setLevel(level)

        ch = logging.StreamHandler(None)
        ch.setLevel(level)

        # create formatter
        if level == logging.INFO:
            formatter = logging.Formatter(InfoFmtString)
        else:
            formatter = logging.Formatter(DebugFmtString)

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        log.addHandler(ch)

    def _create_event_sources(self):
        if 'event_sources' in self.config['lambda']:
            for event_source_cfg in self.config['lambda']['event_sources']:
                _, _, svc, _ = event_source_cfg['arn'].split(':', 3)
                if svc == 'kinesis':
                    self.event_sources.append(
                        kappa.event_source.KinesisEventSource(
                            self, event_source_cfg))
                elif svc == 's3':
                    self.event_sources.append(kappa.event_source.S3EventSource(
                        self, event_source_cfg))
                elif svc == 'sns':
                    self.event_sources.append(
                        kappa.event_source.SNSEventSource(
                            self, event_source_cfg))
                elif svc == 'dynamodb':
                    self.event_sources.append(
                        kappa.event_source.DynamoDBStreamEventSource(
                            self, event_source_cfg))
                else:
                    msg = 'Unknown event source: %s' % event_source_cfg['arn']
                    raise ValueError(msg)

    def add_event_sources(self):
        for event_source in self.event_sources:
            event_source.add(self.function)

    def update_event_sources(self):
        for event_source in self.event_sources:
            event_source.update(self.function)

    def create(self):
        if self.policy:
            self.policy.create()
        if self.role:
            self.role.create()
        # There is a consistency problem here.
        # If you don't wait for a bit, the function.create call
        # will fail because the policy has not been attached to the role.
        LOG.debug('Waiting for policy/role propogation')
        time.sleep(5)
        self.function.create()

    def update_code(self):
        self.function.update()

    def invoke(self):
        return self.function.invoke()

    def dryrun(self):
        return self.function.dryrun()

    def invoke_async(self):
        return self.function.invoke_async()

    def tail(self):
        return self.function.tail()

    def delete(self):
        for event_source in self.event_sources:
            event_source.remove(self.function)
        self.function.delete()
        time.sleep(5)
        if self.role:
            self.role.delete()
        time.sleep(5)
        if self.policy:
            self.policy.delete()

    def status(self):
        status = {}
        if self.policy:
            status['policy'] = self.policy.status()
        else:
            status['policy'] = None
        if self.role:
            status['role'] = self.role.status()
        else:
            status['role'] = None
        status['function'] = self.function.status()
        status['event_sources'] = []
        if self.event_sources:
            for event_source in self.event_sources:
                status['event_sources'].append(
                    event_source.status(self.function))
        return status
