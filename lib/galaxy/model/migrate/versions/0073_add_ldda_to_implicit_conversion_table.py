"""
Migration script to add 'ldda_parent_id' column to the implicitly_converted_dataset_association table.
"""

import logging

from sqlalchemy import Column, ForeignKey, Integer, MetaData, Table

log = logging.getLogger(__name__)
metadata = MetaData()


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    print(__doc__)
    metadata.reflect()
<<<<<<< HEAD
    try:
        Implicitly_converted_table = Table("implicitly_converted_dataset_association", metadata, autoload=True)
        if migrate_engine.name != 'sqlite':
            c = Column("ldda_parent_id", Integer, ForeignKey("library_dataset_dataset_association.id"), index=True, nullable=True)
        else:
            # Can't use the ForeignKey in sqlite.
            c = Column("ldda_parent_id", Integer, index=True, nullable=True)
        c.create(Implicitly_converted_table, index_name="ix_implicitly_converted_dataset_assoc_ldda_parent_id")
        assert c is Implicitly_converted_table.c.ldda_parent_id
    except Exception:
        log.exception("Adding ldda_parent_id column to implicitly_converted_dataset_association table failed.")
=======

    c = Column("ldda_parent_id", Integer, ForeignKey("library_dataset_dataset_association.id"), index=True, nullable=True)
    add_column(c, 'implicitly_converted_dataset_association', metadata, index_name='ix_implicitly_converted_dataset_assoc_ldda_parent_id')
>>>>>>> refs/heads/release_21.01


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.reflect()
    try:
        Implicitly_converted_table = Table("implicitly_converted_dataset_association", metadata, autoload=True)
        Implicitly_converted_table.c.ldda_parent_id.drop()
    except Exception:
        log.exception("Dropping ldda_parent_id column from implicitly_converted_dataset_association table failed.")
