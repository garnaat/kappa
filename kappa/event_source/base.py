# -*- coding: utf-8 -*-
# Copyright (c) 2014, 2015 Mitch Garnaat
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


class EventSource(object):

    def __init__(self, context, config):
        self._context = context
        self._config = config

    @property
    def arn(self):
        return self._config['arn']

    @property
    def starting_position(self):
        return self._config.get('starting_position', 'LATEST')

    @property
    def batch_size(self):
        return self._config.get('batch_size', 100)

    @property
    def batch_window(self):
        return self._config.get('batch_window', 0)

    @property
    def enabled(self):
        return self._config.get('enabled', False)
