"""
Add a user_id column to the job table.
"""

import logging

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    Table
)

<<<<<<< HEAD
=======
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
    metadata.reflect()
<<<<<<< HEAD
=======

    Job_table = Table("job", metadata, autoload=True)
    col = Column("user_id", Integer, ForeignKey("galaxy_user.id"), index=True, nullable=True)
    add_column(col, Job_table, metadata, index_name='ix_job_user_id')
>>>>>>> refs/heads/release_21.01
    try:
<<<<<<< HEAD
        Job_table = Table("job", metadata, autoload=True)
    except NoSuchTableError:
        Job_table = None
        log.debug("Failed loading table job")
    if Job_table is not None:

        if migrate_engine.name != 'sqlite':
            try:
                col = Column("user_id", Integer, ForeignKey("galaxy_user.id"), index=True, nullable=True)
                col.create(Job_table, index_name='ix_job_user_id')
                assert col is Job_table.c.user_id
            except Exception:
                log.exception("Adding column 'user_id' to job table failed.")
        else:
            try:
                col = Column("user_id", Integer, nullable=True)
                col.create(Job_table)
                assert col is Job_table.c.user_id
            except Exception:
                log.exception("Adding column 'user_id' to job table failed.")
        try:
            cmd = "SELECT job.id AS galaxy_job_id, " \
                + "galaxy_session.user_id AS galaxy_user_id " \
                + "FROM job " \
                + "JOIN galaxy_session ON job.session_id = galaxy_session.id;"
            job_users = migrate_engine.execute(cmd).fetchall()
            print("Updating user_id column in job table for ", len(job_users), " rows...")
            print("")
            update_count = 0
            for row in job_users:
                if row.galaxy_user_id:
                    cmd = "UPDATE job SET user_id = %d WHERE id = %d" % (int(row.galaxy_user_id), int(row.galaxy_job_id))
                    update_count += 1
                migrate_engine.execute(cmd)
            print("Updated the user_id column for ", update_count, " rows in the job table.  ")
            print(len(job_users) - update_count, " rows have no user_id since the value was NULL in the galaxy_session table.")
            print("")
        except Exception:
            log.exception("Updating job.user_id column failed.")
=======
        cmd = "SELECT job.id AS galaxy_job_id, " \
            + "galaxy_session.user_id AS galaxy_user_id " \
            + "FROM job " \
            + "JOIN galaxy_session ON job.session_id = galaxy_session.id;"
        job_users = migrate_engine.execute(cmd).fetchall()
        print("Updating user_id column in job table for ", len(job_users), " rows...")
        print("")
        update_count = 0
        for row in job_users:
            if row.galaxy_user_id:
                cmd = "UPDATE job SET user_id = %d WHERE id = %d" % (int(row.galaxy_user_id), int(row.galaxy_job_id))
                update_count += 1
            migrate_engine.execute(cmd)
        print("Updated column 'user_id' for ", update_count, " rows of table 'job'.")
        print(len(job_users) - update_count, " rows have no user_id since the value was NULL in the galaxy_session table.")
        print("")
    except Exception:
        log.exception("Updating column 'user_id' of table 'job' failed.")
>>>>>>> refs/heads/release_21.01


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.reflect()
    try:
        Job_table = Table("job", metadata, autoload=True)
        col = Job_table.c.user_id
        col.drop()
    except Exception:
        log.exception("Dropping column 'user_id' from job table failed.")
