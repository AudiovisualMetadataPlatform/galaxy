<<<<<<< HEAD
=======
"""
"""

>>>>>>> refs/heads/release_21.01
import logging

from sqlalchemy import Index, MetaData, Table

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
    print(__doc__)
    metadata.bind = migrate_engine
    User_table = Table("galaxy_user", metadata, autoload=True)
<<<<<<< HEAD
    HistoryDatasetAssociation_table = Table("history_dataset_association", metadata, autoload=True)
    # Load existing tables
    metadata.reflect()
    # Add 2 indexes to the galaxy_user table
    i = Index('ix_galaxy_user_deleted', User_table.c.deleted)
    try:
        i.create()
    except Exception:
        log.exception("Adding index 'ix_galaxy_user_deleted' to galaxy_user table failed.")
    i = Index('ix_galaxy_user_purged', User_table.c.purged)
    try:
        i.create()
    except Exception:
        log.exception("Adding index 'ix_galaxy_user_purged' to galaxy_user table failed.")
=======
    # The next add_index() calls are not needed any more after commit
    # 7ee93c0995123b0f357abd649326295dfa06766c , but harmless
    add_index('ix_galaxy_user_deleted', User_table, 'deleted')
    add_index('ix_galaxy_user_purged', User_table, 'purged')
>>>>>>> refs/heads/release_21.01
    # Set the default data in the galaxy_user table, but only for null values
    cmd = "UPDATE galaxy_user SET deleted = %s WHERE deleted is null" % engine_false(migrate_engine)
    try:
        migrate_engine.execute(cmd)
    except Exception:
        log.exception("Setting default data for galaxy_user.deleted column failed.")
    cmd = "UPDATE galaxy_user SET purged = %s WHERE purged is null" % engine_false(migrate_engine)
    try:
        migrate_engine.execute(cmd)
    except Exception:
        log.exception("Setting default data for galaxy_user.purged column failed.")
    # Add 1 index to the history_dataset_association table
    i = Index('ix_hda_copied_from_library_dataset_dataset_association_id', HistoryDatasetAssociation_table.c.copied_from_library_dataset_dataset_association_id)
    try:
        i.create()
    except Exception:
        log.exception("Adding index 'ix_hda_copied_from_library_dataset_dataset_association_id' to history_dataset_association table failed.")


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    pass
