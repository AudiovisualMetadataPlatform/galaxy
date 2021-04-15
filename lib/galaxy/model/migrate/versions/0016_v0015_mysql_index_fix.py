"""
This script was used to fix a problem introduced in 0015_tagging.py. MySQL has a
name length limit and thus the index "ix_hda_ta_history_dataset_association_id"
had to be manually created.

This is now fixed in SQLAlchemy Migrate.
"""

import logging

<<<<<<< HEAD
from sqlalchemy import Column, ForeignKey, Index, Integer, MetaData, Table
=======
from sqlalchemy import (
    MetaData,
    Table
)
>>>>>>> refs/heads/release_21.01

# Need our custom types, but don't import anything else from model
from galaxy.model.custom_types import TrimmedString

log = logging.getLogger(__name__)
metadata = MetaData()


HistoryDatasetAssociationTagAssociation_table = Table("history_dataset_association_tag_association", metadata,
                                                      Column("history_dataset_association_id", Integer, ForeignKey("history_dataset_association.id"), index=True),
                                                      Column("tag_id", Integer, ForeignKey("tag.id"), index=True),
                                                      Column("user_tname", TrimmedString(255), index=True),
                                                      Column("value", TrimmedString(255), index=True),
                                                      Column("user_value", TrimmedString(255), index=True))

<<<<<<< HEAD

def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    print(__doc__)
    metadata.reflect()
    i = Index("ix_hda_ta_history_dataset_association_id", HistoryDatasetAssociationTagAssociation_table.c.history_dataset_association_id)
    try:
        i.create()
    except Exception:
        log.exception("Adding index 'ix_hdata_history_dataset_association_id' to table 'history_dataset_association_tag_association' table failed.")
=======
    HistoryDatasetAssociationTagAssociation_table = Table('history_dataset_association_tag_association', metadata, autoload=True)
    if not any([_.name for _ in index.columns] == ['history_dataset_association_id'] for index in HistoryDatasetAssociationTagAssociation_table.indexes):
        add_index('ix_hda_ta_history_dataset_association_id', HistoryDatasetAssociationTagAssociation_table, 'history_dataset_association_id')
>>>>>>> refs/heads/release_21.01


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.reflect()
    i = Index("ix_hda_ta_history_dataset_association_id", HistoryDatasetAssociationTagAssociation_table.c.history_dataset_association_id)
    try:
        i.drop()
    except Exception:
        log.exception("Removing index 'ix_hdata_history_dataset_association_id' to table 'history_dataset_association_tag_association' table failed.")
