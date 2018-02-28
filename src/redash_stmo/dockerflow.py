# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import absolute_import
import logging

from dockerflow.flask import Dockerflow
from redash import migrate, redis_connection
from redash.models import db

logger = logging.getLogger(__name__)


def dockerflow(app):
    logger.info('Loading Redash Extension for Dockerflow')
    dockerflow = Dockerflow(app, db=db, migrate=migrate, redis=redis_connection)
    logger.info('Loaded Redash Extension for Dockerflow')
    return dockerflow
