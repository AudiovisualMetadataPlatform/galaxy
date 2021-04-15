"""
Migration script to add column for a history slug.
"""

import logging

from sqlalchemy import (
    Column,
    MetaData,
    Table,
    TEXT
)

<<<<<<< HEAD
=======
from galaxy.model.migrate.versions.util import (
    add_column,
    add_index,
    drop_column
)

>>>>>>> refs/heads/release_21.01
log = logging.getLogger(__name__)
metadata = MetaData()


def upgrade(migrate_engine):
    metadata.bind = migrate_engine

    print(__doc__)
    metadata.reflect()

    History_table = Table("history", metadata, autoload=True)
    c = Column("slug", TEXT)
    add_column(c, History_table, metadata)
    # Index needs to be added separately because MySQL cannot index a TEXT/BLOB
    # column without specifying mysql_length
    add_index('ix_history_slug', History_table, 'slug')


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.reflect()

    History_table = Table("history", metadata, autoload=True)
    History_table.c.slug.drop()
