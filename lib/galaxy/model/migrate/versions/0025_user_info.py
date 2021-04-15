"""
This script adds a foreign key to the form_values table in the galaxy_user table
"""

import logging

<<<<<<< HEAD
from migrate import ForeignKeyConstraint
from sqlalchemy import Column, Integer, MetaData, Table
from sqlalchemy.exc import NoSuchTableError
=======
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData
)

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
    # Load existing tables
    metadata.reflect()
<<<<<<< HEAD
    try:
        User_table = Table("galaxy_user", metadata, autoload=True)
    except NoSuchTableError:
        User_table = None
        log.debug("Failed loading table galaxy_user")
    if User_table is not None:
        try:
            col = Column("form_values_id", Integer, index=True)
            col.create(User_table, index_name='ix_user_form_values_id')
            assert col is User_table.c.form_values_id
        except Exception:
            log.exception("Adding column 'form_values_id' to galaxy_user table failed.")
        try:
            FormValues_table = Table("form_values", metadata, autoload=True)
        except NoSuchTableError:
            FormValues_table = None
            log.debug("Failed loading table form_values")
        if migrate_engine.name != 'sqlite':
            # Add 1 foreign key constraint to the form_values table
            if User_table is not None and FormValues_table is not None:
                try:
                    cons = ForeignKeyConstraint([User_table.c.form_values_id],
                                                [FormValues_table.c.id],
                                                name='user_form_values_id_fk')
                    # Create the constraint
                    cons.create()
                except Exception:
                    log.exception("Adding foreign key constraint 'user_form_values_id_fk' to table 'galaxy_user' failed.")
=======

    col = Column("form_values_id", Integer, ForeignKey('form_values.id', name='user_form_values_id_fk'), index=True)
    add_column(col, 'galaxy_user', metadata, index_name='ix_galaxy_user_form_values_id')
>>>>>>> refs/heads/release_21.01


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    pass
