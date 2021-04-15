"""
Postponed to migration 160.
"""
<<<<<<< HEAD
from __future__ import print_function

import logging

log = logging.getLogger(__name__)
=======
>>>>>>> refs/heads/release_21.01


def engine_true(migrate_engine):
    if migrate_engine.name in ['postgres', 'postgresql']:
        return "TRUE"
    elif migrate_engine.name in ['mysql', 'sqlite']:
        return 1
    else:
        raise Exception('Unknown database type: %s' % migrate_engine.name)


def upgrade(migrate_engine):
    print(__doc__)


def downgrade(migrate_engine):
    pass
