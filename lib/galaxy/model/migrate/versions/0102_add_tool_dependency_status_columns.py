"""
Migration script to add status and error_message columns to the tool_dependency table and drop the uninstalled column from the tool_dependency table.
"""

import logging

from sqlalchemy import (
    Boolean,
    Column,
    MetaData,
    Table,
    TEXT
)

# Need our custom types, but don't import anything else from model
from galaxy.model.custom_types import TrimmedString
<<<<<<< HEAD
=======
from galaxy.model.migrate.versions.util import (
    add_column,
    drop_column
)
>>>>>>> refs/heads/release_21.01

log = logging.getLogger(__name__)
metadata = MetaData()


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    print(__doc__)
    metadata.reflect()
    ToolDependency_table = Table("tool_dependency", metadata, autoload=True)
    if migrate_engine.name == 'sqlite':
        col = Column("status", TrimmedString(255))
    else:
        col = Column("status", TrimmedString(255), nullable=False)
<<<<<<< HEAD
    try:
        col.create(ToolDependency_table)
        assert col is ToolDependency_table.c.status
    except Exception:
        log.exception("Adding status column to the tool_dependency table failed.")
=======
    add_column(col, ToolDependency_table, metadata)

>>>>>>> refs/heads/release_21.01
    col = Column("error_message", TEXT)
<<<<<<< HEAD
    try:
        col.create(ToolDependency_table)
        assert col is ToolDependency_table.c.error_message
    except Exception:
        log.exception("Adding error_message column to the tool_dependency table failed.")
=======
    add_column(col, ToolDependency_table, metadata)
>>>>>>> refs/heads/release_21.01

    if migrate_engine.name != 'sqlite':
        # This breaks in sqlite due to failure to drop check constraint.
        # TODO move to alembic.
        try:
            ToolDependency_table.c.uninstalled.drop()
        except Exception:
            log.exception("Dropping uninstalled column from the tool_dependency table failed.")


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.reflect()
    ToolDependency_table = Table("tool_dependency", metadata, autoload=True)
<<<<<<< HEAD
    try:
        ToolDependency_table.c.status.drop()
    except Exception:
        log.exception("Dropping column status from the tool_dependency table failed.")
    try:
        ToolDependency_table.c.error_message.drop()
    except Exception:
        log.exception("Dropping column error_message from the tool_dependency table failed.")
    col = Column("uninstalled", Boolean, default=False)
    try:
        col.create(ToolDependency_table)
        assert col is ToolDependency_table.c.uninstalled
    except Exception:
        log.exception("Adding uninstalled column to the tool_dependency table failed.")
=======
    if migrate_engine.name != 'sqlite':
        col = Column("uninstalled", Boolean, default=False)
        add_column(col, ToolDependency_table, metadata)

    drop_column('error_message', ToolDependency_table)
    drop_column('status', ToolDependency_table)
>>>>>>> refs/heads/release_21.01
