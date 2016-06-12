# -*- coding: utf-8 -*-
import logging
import json
import uuid

import boto3

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

# The kappa deploy command will make sure that the right config file
# for this environment is available in the local directory.
config = json.load(open('config.json'))

session = boto3.Session(region_name=config['region_name'])
ddb_client = session.resource('dynamodb')
table = ddb_client.Table(config['sample_table'])


def foobar():
    return 42


def _get(event, context):
    assert context
    customer_id = event.get('id')
    if customer_id is None:
        raise Exception('No id provided for GET operation')
    response = table.get_item(Key={'id': customer_id})
    item = response.get('Item')
    if item is None:
        raise Exception('id: {} not found'.format(customer_id))
    return response['Item']


def _post(event, context):
    assert context
    item = event['json_body']
    if item is None:
        raise Exception('No json_body found in event')
    item['id'] = str(uuid.uuid4())
    table.put_item(Item=item)
    return item


def _put(event, context):
    assert context
    data = _get(event, context)
    id_ = data.get('id')
    data.update(event['json_body'])
    # don't allow the id to be changed
    data['id'] = id_
    table.put_item(Item=data)
    return data


def handler(event, context):
    assert context
    LOG.info(event)
    http_method = event.get('http_method')
    if not http_method:
        return 'NoHttpMethodSupplied'
    if http_method == 'GET':
        return _get(event, context)
    elif http_method == 'POST':
        return _post(event, context)
    elif http_method == 'PUT':
        return _put(event, context)
    elif http_method == 'DELETE':
        return _put(event, context)
    else:
        raise Exception('UnsupportedMethod: {}'.format(http_method))
