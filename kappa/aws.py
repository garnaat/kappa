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

import botocore.session


class __AWS(object):

    def __init__(self, profile=None, region=None):
        self._client_cache = {}
        self._session = botocore.session.get_session()
        self._session.profile = profile
        self._region = region

    def create_client(self, client_name):
        if client_name not in self._client_cache:
            self._client_cache[client_name] = self._session.create_client(
                client_name, self._region)
        return self._client_cache[client_name]


__Singleton_AWS = None


def get_aws(context):
    global __Singleton_AWS
    if __Singleton_AWS is None:
        __Singleton_AWS = __AWS(context.profile, context.region)
    return __Singleton_AWS
