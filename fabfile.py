# coding: utf-8
from fabric.api import task, env
from unipath import Path
from jetpack.helpers import Project

# Exposes other functionalities
from jetpack import setup, deploy, db, config, django, logs, pg_backups


# Always run fabric from the repository root dir.
Path(__file__).parent.chdir()

@task
def digital_ocean():
    env.PROJECT = Project(project='vivo_scrapper', instance='production')
    env.hosts = ['104.131.127.200']
    env.user = env.PROJECT.user
