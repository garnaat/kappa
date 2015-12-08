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
import os

import jmespath
import boto3
import placebo


LOG = logging.getLogger(__name__)


class AWSClient(object):

    def __init__(self, service_name, region_name, profile_name):
        self._service_name = service_name
        self._region_name = region_name
        self._profile_name = profile_name
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

    def _create_client(self):
        session = boto3.session.Session(
            region_name=self._region_name, profile_name=self._profile_name)
        placebo.attach(session)
        client = session.client(self._service_name)
        return client

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
        return data


_client_cache = {}


def save_recordings(recording_path):
    for key in _client_cache:
        client = _client_cache[key]
        full_path = os.path.join(recording_path, '{}.json'.format(key))
        client._client.meta.placebo.save(full_path)


def create_client(service_name, context):
    global _client_cache
    client_key = '{}:{}:{}'.format(service_name, context.region,
                                   context.profile)
    if client_key not in _client_cache:
        client = AWSClient(service_name, context.region,
                           context.profile)
        if 'placebo' in context.config:
            placebo_cfg = context.config['placebo']
            if placebo_cfg.get('mode') == 'play':
                full_path = os.path.join(
                    placebo_cfg['recording_path'],
                    '{}.json'.format(client_key))
                if os.path.exists(full_path):
                    client._client.meta.placebo.load(full_path)
                client._client.meta.placebo.start()
            elif placebo_cfg['mode'] == 'record':
                client._client.meta.placebo.record()
        _client_cache[client_key] = client
    return _client_cache[client_key]
