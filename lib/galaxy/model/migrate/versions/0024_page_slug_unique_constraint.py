"""
Remove unique constraint from page slugs to allow creating a page with
the same slug as a deleted page.
"""

import logging

from sqlalchemy import (
    MetaData,
    Table
)

from galaxy.model.migrate.versions.util import (
    add_index,
    drop_index
)

log = logging.getLogger(__name__)
metadata = MetaData()


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    print(__doc__)
    metadata.reflect()

    Page_table = Table("page", metadata, autoload=True)

    try:

        # Sqlite doesn't support .alter, so we need to drop an recreate
<<<<<<< HEAD

        i = Index("ix_page_slug", Page_table.c.slug)
        i.drop()
=======
        drop_index("ix_page_slug", Page_table, 'slug')
>>>>>>> refs/heads/release_21.01

<<<<<<< HEAD
        i = Index("ix_page_slug", Page_table.c.slug, unique=False)
        i.create()

=======
        add_index("ix_page_slug", Page_table, 'slug', unique=False)
>>>>>>> refs/heads/release_21.01
    except Exception:

        # Mysql doesn't have a named index, but alter should work

        Page_table.c.slug.alter(unique=False)


def downgrade(migrate_engine):
    pass
