"""
This script fixes a problem introduced in the previous migration script
0010_hda_display_at_authz_table.py .  MySQL has a name length limit and
thus the index "ix_hdadaa_history_dataset_association_id" has to be
manually created.
"""

import datetime
import logging

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, MetaData, Table

# Need our custom types, but don't import anything else from model
from galaxy.model.custom_types import TrimmedString

log = logging.getLogger(__name__)
now = datetime.datetime.utcnow
metadata = MetaData()

HistoryDatasetAssociationDisplayAtAuthorization_table = Table("history_dataset_association_display_at_authorization", metadata,
                                                              Column("id", Integer, primary_key=True),
                                                              Column("create_time", DateTime, default=now),
                                                              Column("update_time", DateTime, index=True, default=now, onupdate=now),
                                                              Column("history_dataset_association_id", Integer, ForeignKey("history_dataset_association.id"), index=True),
                                                              Column("user_id", Integer, ForeignKey("galaxy_user.id"), index=True),
                                                              Column("site", TrimmedString(255)))


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    print(__doc__)
    if migrate_engine.name == 'mysql':
        # Load existing tables
        metadata.reflect()
        i = Index("ix_hdadaa_history_dataset_association_id", HistoryDatasetAssociationDisplayAtAuthorization_table.c.history_dataset_association_id)
        try:
            i.create()
        except Exception:
            log.exception("Adding index 'ix_hdadaa_history_dataset_association_id' to table 'history_dataset_association_display_at_authorization' table failed.")


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    if migrate_engine.name == 'mysql':
        # Load existing tables
        metadata.reflect()
        i = Index("ix_hdadaa_history_dataset_association_id", HistoryDatasetAssociationDisplayAtAuthorization_table.c.history_dataset_association_id)
        try:
            i.drop()
        except Exception:
            log.exception("Removing index 'ix_hdadaa_history_dataset_association_id' from table 'history_dataset_association_display_at_authorization' table failed.")
