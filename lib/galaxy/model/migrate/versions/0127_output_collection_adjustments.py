"""
Migration script updating collections tables for output collections.
"""

import logging

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    Table,
    TEXT,
    Unicode
)

from galaxy.model.custom_types import TrimmedString
<<<<<<< HEAD
=======
from galaxy.model.migrate.versions.util import (
    add_column,
    create_table,
    drop_column,
    drop_table
)
>>>>>>> refs/heads/release_21.01

log = logging.getLogger(__name__)
metadata = MetaData()

JobToImplicitOutputDatasetCollectionAssociation_table = Table(
    "job_to_implicit_output_dataset_collection", metadata,
    Column("id", Integer, primary_key=True),
    Column("job_id", Integer, ForeignKey("job.id"), index=True),
    Column("dataset_collection_id", Integer, ForeignKey("dataset_collection.id"), index=True),
    Column("name", Unicode(255))
)


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    print(__doc__)
    metadata.reflect()

<<<<<<< HEAD
    for table in TABLES:
        __create(table)
=======
    create_table(JobToImplicitOutputDatasetCollectionAssociation_table)
>>>>>>> refs/heads/release_21.01

<<<<<<< HEAD
    try:
        dataset_collection_table = Table("dataset_collection", metadata, autoload=True)
        # need server_default because column in non-null
        populated_state_column = Column('populated_state', TrimmedString(64), default='ok', server_default="ok", nullable=False)
        populated_state_column.create(dataset_collection_table)
=======
    dataset_collection_table = Table("dataset_collection", metadata, autoload=True)
    # need server_default because column in non-null
    populated_state_column = Column('populated_state', TrimmedString(64), default='ok', server_default="ok", nullable=False)
    add_column(populated_state_column, dataset_collection_table, metadata)
>>>>>>> refs/heads/release_21.01

<<<<<<< HEAD
        populated_message_column = Column('populated_state_message', TEXT, nullable=True)
        populated_message_column.create(dataset_collection_table)
    except Exception:
        log.exception("Creating dataset collection populated column failed.")
=======
    populated_message_column = Column('populated_state_message', TEXT, nullable=True)
    add_column(populated_message_column, dataset_collection_table, metadata)
>>>>>>> refs/heads/release_21.01


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.reflect()

<<<<<<< HEAD
    for table in TABLES:
        __drop(table)
=======
    drop_table(JobToImplicitOutputDatasetCollectionAssociation_table)
>>>>>>> refs/heads/release_21.01

    try:
        dataset_collection_table = Table("dataset_collection", metadata, autoload=True)
        populated_state_column = dataset_collection_table.c.populated_state
        populated_state_column.drop()
        populated_message_column = dataset_collection_table.c.populated_state_message
        populated_message_column.drop()
    except Exception:
        log.exception("Dropping dataset collection populated_state/ column failed.")


def __create(table):
    try:
        table.create()
    except Exception:
        log.exception("Creating %s table failed.", table.name)


def __drop(table):
    try:
        table.drop()
    except Exception:
        log.exception("Dropping %s table failed.", table.name)
