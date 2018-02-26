import logging

from dockerflow.flask import Dockerflow
from redash import migrate, redis_connection
from redash.models import db

logger = logging.getLogger(__name__)


def dockerflow(app):
    logger.info('Loading Redash Extension for Dockerflow')
    Dockerflow(app, db=db, migrate=migrate, redis=redis_connection)
    logger.info('Loaded Redash Extension for Dockerflow')
