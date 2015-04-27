import inspect

import mock

import tests.unit.responses as responses


class MockAWS(object):

    def __init__(self, profile=None, region=None):
        self.response_map = {}
        for name, value in inspect.getmembers(responses):
            if name.startswith('__'):
                continue
            if '_' in name:
                service_name, request_name = name.split('_', 1)
                if service_name not in self.response_map:
                    self.response_map[service_name] = {}
                self.response_map[service_name][request_name] = value

    def create_client(self, client_name):
        client = None
        if client_name in self.response_map:
            client = mock.Mock()
            for request in self.response_map[client_name]:
                response = self.response_map[client_name][request]
                setattr(client, request, mock.Mock(side_effect=response))
        return client


def get_aws(context):
    return MockAWS()
