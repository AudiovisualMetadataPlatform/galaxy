"""
Migration script to add dbkey column for visualization.
"""

import logging
from json import loads

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

    Visualization_table = Table("visualization", metadata, autoload=True)
    Visualization_revision_table = Table("visualization_revision", metadata, autoload=True)

    # Create dbkey columns.
    x = Column("dbkey", TEXT)
<<<<<<< HEAD
=======
    add_column(x, Visualization_table, metadata)
>>>>>>> refs/heads/release_21.01
    y = Column("dbkey", TEXT)
<<<<<<< HEAD
    x.create(Visualization_table)
    y.create(Visualization_revision_table)
    # Manually create indexes for compatability w/ mysql_length.
    xi = Index("ix_visualization_dbkey", Visualization_table.c.dbkey, mysql_length=200)
    xi.create()
    yi = Index("ix_visualization_revision_dbkey", Visualization_revision_table.c.dbkey, mysql_length=200)
    yi.create()
    assert x is Visualization_table.c.dbkey
    assert y is Visualization_revision_table.c.dbkey
=======
    add_column(y, Visualization_revision_table, metadata)
    # Indexes need to be added separately because MySQL cannot index a TEXT/BLOB
    # column without specifying mysql_length
    add_index("ix_visualization_dbkey", Visualization_table, 'dbkey')
    add_index("ix_visualization_revision_dbkey", Visualization_revision_table, 'dbkey')
>>>>>>> refs/heads/release_21.01

    all_viz = migrate_engine.execute("SELECT visualization.id as viz_id, visualization_revision.id as viz_rev_id, visualization_revision.config FROM visualization_revision \
                    LEFT JOIN visualization ON visualization.id=visualization_revision.visualization_id")
    for viz in all_viz:
        viz_id = viz['viz_id']
        viz_rev_id = viz['viz_rev_id']
        if viz[Visualization_revision_table.c.config]:
            dbkey = loads(viz[Visualization_revision_table.c.config]).get('dbkey', "").replace("'", "\\'")
            migrate_engine.execute(f"UPDATE visualization_revision SET dbkey='{dbkey}' WHERE id={viz_rev_id}")
            migrate_engine.execute(f"UPDATE visualization SET dbkey='{dbkey}' WHERE id={viz_id}")


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.reflect()

    Visualization_table = Table("visualization", metadata, autoload=True)
    Visualization_revision_table = Table("visualization_revision", metadata, autoload=True)

    Visualization_table.c.dbkey.drop()
    Visualization_revision_table.c.dbkey.drop()
