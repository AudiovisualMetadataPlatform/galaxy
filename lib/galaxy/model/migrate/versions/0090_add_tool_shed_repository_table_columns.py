"""
Migration script to add the uninstalled and dist_to_shed columns to the tool_shed_repository table.
"""

import logging

from sqlalchemy import (
    Boolean,
    Column,
    MetaData,
    Table
)

<<<<<<< HEAD
=======
from galaxy.model.migrate.versions.util import (
    add_column,
    drop_column,
    engine_false
)

>>>>>>> refs/heads/release_21.01
log = logging.getLogger(__name__)
metadata = MetaData()


def engine_false(migrate_engine):
    if migrate_engine.name in ['postgres', 'postgresql']:
        return "FALSE"
    elif migrate_engine.name in ['mysql', 'sqlite']:
        return 0
    else:
        raise Exception('Unknown database type: %s' % migrate_engine.name)


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    print(__doc__)
    metadata.reflect()
    ToolShedRepository_table = Table("tool_shed_repository", metadata, autoload=True)
    c = Column("uninstalled", Boolean, default=False)
    add_column(c, ToolShedRepository_table, metadata)
    try:
        migrate_engine.execute("UPDATE tool_shed_repository SET uninstalled=%s" % engine_false(migrate_engine))
    except Exception:
        log.exception("Updating column 'uninstalled' of table 'tool_shed_repository' failed.")
    c = Column("dist_to_shed", Boolean, default=False)
    add_column(c, ToolShedRepository_table, metadata)
    try:
        migrate_engine.execute("UPDATE tool_shed_repository SET dist_to_shed=%s" % engine_false(migrate_engine))
    except Exception:
        log.exception("Updating column 'dist_to_shed' of table 'tool_shed_repository' failed.")


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.reflect()
    ToolShedRepository_table = Table("tool_shed_repository", metadata, autoload=True)
    # SQLAlchemy Migrate has a bug when dropping a boolean column in SQLite
    if migrate_engine.name != 'sqlite':
        try:
            ToolShedRepository_table.c.uninstalled.drop()
        except Exception:
            log.exception("Dropping column uninstalled from the tool_shed_repository table failed.")
        try:
            ToolShedRepository_table.c.dist_to_shed.drop()
        except Exception:
            log.exception("Dropping column dist_to_shed from the tool_shed_repository table failed.")
