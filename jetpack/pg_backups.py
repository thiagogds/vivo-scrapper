# coding: utf-8
import os
from unipath import Path
from fabric.api import task, run, env, require, settings, hide, fastprint, get, put, prompt
from fabric.contrib.files import append, sed
from fabric.contrib.console import confirm


@task
def list():
    """
    List remote backups.
    """
    require('PROJECT')

    fastprint(run('%(current)s/bin/s3cmd --config=%(share)s/s3cfg.ini ls s3://metapix/backup/%(instance)s/' % env.PROJECT))

@task
def restore(name=""):
    """
    Restore backup from S3 by name

    Usage: fab pg_backups.restore:s3://metapix/backup/stage/metapix_stage-2015-01-10-03:00:01
    """

    require('PROJECT')

    if not confirm("Are you sure? This will erase the database!!", default=False):
        return

    if not confirm("Really?", default=False):
        return

    if not name:
        name = run("cat %(checkpoint)s" % env.PROJECT)

    params = dict(env.PROJECT.items() + locals().items())

    run('%(current)s/bin/s3cmd --config=%(share)s/s3cfg.ini get %(name)s %(tmp)s' % params)

    dbname = env.PROJECT.appname
    dbuser = env.PROJECT.appname

    backup_filename = name.split("/")[-1]
    backup_file = os.path.join(env.PROJECT.tmp, backup_filename)

    with settings(warn_only=True):
        run('pg_restore --verbose --clean -U %(dbuser)s -d %(dbname)s %(backup_file)s' % locals())

    # cleanup
    run('rm ' + backup_file)

@task
def checkpoint(name=""):
    """
    Manage checkpoint to automatic restore backups in the future

    Usage:
    fab  pg_backups.checkpoint -> print checkpoint content
    fab  pg_backups.checkpoint:s3://metapix/backup/stage/metapix_stage-2015-01-10-03:00:01 -> update checkpoint content
    """

    if not name:
        fastprint(run("cat %(checkpoint)s" % env.PROJECT))
        return

    params = dict(env.PROJECT.items() + locals().items())

    require('PROJECT')

    run("echo %(name)s > %(checkpoint)s" % params)
