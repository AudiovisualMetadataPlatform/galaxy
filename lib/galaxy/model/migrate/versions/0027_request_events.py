"""
This migration script adds the request_event table and
removes the state field in the request table
"""

import datetime
import logging

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Table,
    TEXT
)

# Need our custom types, but don't import anything else from model
from galaxy.model.custom_types import TrimmedString
<<<<<<< HEAD
=======
from galaxy.model.migrate.versions.util import (
    create_table,
    drop_column,
    localtimestamp,
    nextval
)
>>>>>>> refs/heads/release_21.01

log = logging.getLogger(__name__)
now = datetime.datetime.utcnow
metadata = MetaData()

RequestEvent_table = Table('request_event', metadata,
    Column("id", Integer, primary_key=True),
    Column("create_time", DateTime, default=now),
    Column("update_time", DateTime, default=now, onupdate=now),
    Column("request_id", Integer, ForeignKey("request.id"), index=True),
    Column("state", TrimmedString(255), index=True),
    Column("comment", TEXT))


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    print(__doc__)

<<<<<<< HEAD
    def localtimestamp():
        if migrate_engine.name in ['mysql', 'postgres', 'postgresql']:
            return "LOCALTIMESTAMP"
        elif migrate_engine.name == 'sqlite':
            return "current_date || ' ' || current_time"
        else:
            raise Exception('Unable to convert data for unknown database type: %s' % migrate_engine.name)

    def nextval(table, col='id'):
        if migrate_engine.name in ['postgres', 'postgresql']:
            return "nextval('%s_%s_seq')" % (table, col)
        elif migrate_engine.name in ['mysql', 'sqlite']:
            return "null"
        else:
            raise Exception('Unable to convert data for unknown database type: %s' % migrate_engine.name)
    # Load existing tables
    metadata.reflect()
    # Add new request_event table
    try:
        RequestEvent_table.create()
    except Exception:
        log.exception("Creating request_event table failed.")
=======
    create_table(RequestEvent_table)
>>>>>>> refs/heads/release_21.01
    # move the current state of all existing requests to the request_event table
    cmd = \
        "INSERT INTO request_event " + \
        "SELECT %s AS id," + \
        "%s AS create_time," + \
        "%s AS update_time," + \
        "request.id AS request_id," + \
        "request.state AS state," + \
        "'%s' AS comment " + \
        "FROM request;"
    cmd = cmd % (nextval('request_event'), localtimestamp(), localtimestamp(), 'Imported from request table')
    migrate_engine.execute(cmd)

    drop_column('state', 'request', metadata)


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    pass
