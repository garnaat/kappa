import logging
import time

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)


def handler(event, context):
    LOG.debug(event)
    return {'status': 'success', 'time': time.time()}
