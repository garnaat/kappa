import mock

import tests.unit.responses as responses


class MockAWS(object):

    def __init__(self, profile=None, region=None):
        pass

    def create_client(self, client_name):
        client = None
        if client_name == 'logs':
            client = mock.Mock()
            choices = responses.logs_describe_log_streams
            client.describe_log_streams = mock.Mock(
                side_effect=choices)
            choices = responses.logs_get_log_events
            client.get_log_events = mock.Mock(
                side_effect=choices)
        if client_name == 'cloudformation':
            client = mock.Mock()
            choices = responses.cfn_list_stack_resources
            client.list_stack_resources = mock.Mock(
                side_effect=choices)
            choices = responses.cfn_describe_stacks
            client.describe_stacks = mock.Mock(
                side_effect=choices)
            choices = responses.cfn_create_stack
            client.create_stack = mock.Mock(
                side_effect=choices)
            choices = responses.cfn_delete_stack
            client.delete_stack = mock.Mock(
                side_effect=choices)
        if client_name == 'iam':
            client = mock.Mock()
            choices = responses.iam_get_role
            client.get_role = mock.Mock(
                side_effect=choices)
        return client


def get_aws(context):
    return MockAWS()
