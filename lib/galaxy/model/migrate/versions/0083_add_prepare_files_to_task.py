"""
Migration script to add 'prepare_input_files_cmd' column to the task table and to rename a column.
"""

import logging

from sqlalchemy import Column, MetaData, String, Table, TEXT

log = logging.getLogger(__name__)
metadata = MetaData()


def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    print(__doc__)
    metadata.reflect()
<<<<<<< HEAD
    try:
        task_table = Table("task", metadata, autoload=True)
        c = Column("prepare_input_files_cmd", TEXT, nullable=True)
        c.create(task_table)
        assert c is task_table.c.prepare_input_files_cmd
    except Exception:
        log.exception("Adding prepare_input_files_cmd column to task table failed.")
    try:
        task_table = Table("task", metadata, autoload=True)
        c = Column("working_directory", String(1024), nullable=True)
        c.create(task_table)
        assert c is task_table.c.working_directory
    except Exception:
        log.exception("Adding working_directory column to task table failed.")
=======

    task_table = Table("task", metadata, autoload=True)
    c = Column("prepare_input_files_cmd", TEXT, nullable=True)
    add_column(c, task_table, metadata)

    c = Column("working_directory", String(1024), nullable=True)
    add_column(c, task_table, metadata)
>>>>>>> refs/heads/release_21.01

    # remove the 'part_file' column - nobody used tasks before this, so no data needs to be migrated
    try:
        task_table.c.part_file.drop()
    except Exception:
        log.exception("Deleting column 'part_file' from the 'task' table failed.")


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.reflect()
<<<<<<< HEAD
    try:
        task_table = Table("task", metadata, autoload=True)
        task_table.c.prepare_input_files_cmd.drop()
    except Exception:
        log.exception("Dropping prepare_input_files_cmd column from task table failed.")
    try:
        task_table = Table("task", metadata, autoload=True)
        task_table.c.working_directory.drop()
    except Exception:
        log.exception("Dropping working_directory column from task table failed.")
    try:
        task_table = Table("task", metadata, autoload=True)
        c = Column("part_file", String(1024), nullable=True)
        c.create(task_table)
        assert c is task_table.c.part_file
    except Exception:
        log.exception("Adding part_file column to task table failed.")
=======

    task_table = Table("task", metadata, autoload=True)
    c = Column("part_file", String(1024), nullable=True)
    add_column(c, task_table, metadata)

    drop_column('working_directory', task_table)
    drop_column('prepare_input_files_cmd', task_table)
>>>>>>> refs/heads/release_21.01
