# Copyright (c) 2015 Mitch Garnaat
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import json
import os

import datetime
import jmespath
import boto3


LOG = logging.getLogger(__name__)


def json_encoder(obj):
    """JSON encoder that formats datetimes as ISO8601 format."""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        return obj


class AWSClient(object):

    def __init__(self, service_name, region_name, profile_name,
                 record_path=None):
        self._service_name = service_name
        self._region_name = region_name
        self._profile_name = profile_name
        self._record_path = record_path
        self._client = self._create_client()

    @property
    def service_name(self):
        return self._service_name

    @property
    def region_name(self):
        return self._region_name

    @property
    def profile_name(self):
        return self._profile_name

    def _record(self, op_name, kwargs, data):
        """
        This is a little hack to enable easier unit testing of the code.
        Since botocore/boto3 has its own set of tests, I'm not interested in
        trying to test it again here.  So, this recording capability allows
        us to save the data coming back from botocore as JSON files which
        can then be used by the mocked awsclient in the unit test directory.
        To enable this, pass in a record_path to the contructor and the JSON
        data files will get stored in this path.
        """
        if self._record_path:
            path = os.path.expanduser(self._record_path)
            path = os.path.expandvars(path)
            path = os.path.join(path, self.service_name)
            if not os.path.isdir(path):
                os.mkdir(path)
            path = os.path.join(path, self.region_name)
            if not os.path.isdir(path):
                os.mkdir(path)
            path = os.path.join(path, self.account_id)
            if not os.path.isdir(path):
                os.mkdir(path)
            filename = op_name
            if kwargs:
                for k, v in kwargs.items():
                    if k != 'query':
                        filename += '_{}_{}'.format(k, v)
            filename += '.json'
            path = os.path.join(path, filename)
            with open(path, 'wb') as fp:
                json.dump(data, fp, indent=4, default=json_encoder,
                          ensure_ascii=False)

    def _create_client(self):
        session = boto3.session.Session(
            region_name=self._region_name, profile_name=self._profile_name)
        return session.client(self._service_name)

    def call(self, op_name, query=None, **kwargs):
        """
        Make a request to a method in this client.  The response data is
        returned from this call as native Python data structures.

        This method differs from just calling the client method directly
        in the following ways:

          * It automatically handles the pagination rather than
            relying on a separate pagination method call.
          * You can pass an optional jmespath query and this query
            will be applied to the data returned from the low-level
            call.  This allows you to tailor the returned data to be
            exactly what you want.

        :type op_name: str
        :param op_name: The name of the request you wish to make.

        :type query: str
        :param query: A jmespath query that will be applied to the
            data returned by the operation prior to returning
            it to the user.

        :type kwargs: keyword arguments
        :param kwargs: Additional keyword arguments you want to pass
            to the method when making the request.
        """
        LOG.debug(kwargs)
        if query:
            query = jmespath.compile(query)
        if self._client.can_paginate(op_name):
            paginator = self._client.get_paginator(op_name)
            results = paginator.paginate(**kwargs)
            data = results.build_full_result()
        else:
            op = getattr(self._client, op_name)
            data = op(**kwargs)
        if query:
            data = query.search(data)
        self._record(op_name, kwargs, data)
        return data


_client_cache = {}


def create_client(service_name, context):
    global _client_cache
    client_key = '{}:{}:{}'.format(service_name, context.region,
                                   context.profile)
    if client_key not in _client_cache:
        _client_cache[client_key] = AWSClient(service_name,
                                              context.region,
                                              context.profile,
                                              context.record_path)
    return _client_cache[client_key]
