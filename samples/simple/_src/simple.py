# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)


def handler(event, context):
    assert context
    LOG.debug(event)
    return {'status': 'success'}
