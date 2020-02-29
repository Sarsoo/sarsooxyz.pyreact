from .sarsoo import app

import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

fmframework_logger = logging.getLogger('fmframework')

if os.environ.get('DEPLOY_DESTINATION', None) == 'PROD':
    import google.cloud.logging
    from google.cloud.logging.handlers import CloudLoggingHandler, setup_logging

    log_format = '%(funcName)s - %(message)s'
    formatter = logging.Formatter(log_format)

    client = google.cloud.logging.Client()
    handler = CloudLoggingHandler(client, name="sarsooxyz")

    handler.setFormatter(formatter)

    logger.addHandler(handler)
    fmframework_logger.addHandler(handler)

else:
    log_format = '%(levelname)s %(name)s:%(funcName)s - %(message)s'
    formatter = logging.Formatter(log_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    fmframework_logger.addHandler(stream_handler)
