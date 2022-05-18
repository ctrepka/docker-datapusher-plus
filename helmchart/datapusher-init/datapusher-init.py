import os
import sys

TEST = os.environ.get("TEST", "DEFAULT ENV VALUE")
VENV = os.environ.get("VENV", "/")

os.system(
    "{}/bin/pip install psycopg2-binary".format(VENV)
)

master_user = os.environ.get("POSTGRES_USER", "postgres")
host = os.environ.get("DATAPUSHER_SQLALCHEMY_DATABASE_URI", "")
master_passwd = os.environ.get("POSTGRES_PASSWORD")
# Designed/intended for use with mdillon:11 postgis image.
# See https://hub.docker.com/r/mdillon/postgis/
# for notes on default environment variable settings,
# which are taken into account below
master_database = os.environ.get("POSTGRES_DB", master_user)

import psycopg2

def check_db_connection(db_params, retry=None):

    print('Checking whether database is up...')

    if retry is None:
        retry = 20
    elif retry == 0:
        print('Giving up...')
        sys.exit(1)

    try:
        con = psycopg2.connect(user=master_user,
                               host=db_params.db_host,
                               password=master_passwd,
                               database=master_database)

    except psycopg2.Error as e:
        print((str(e)))
        print('Unable to connect to the database...try again in a while.')
        import time
        time.sleep(30)
        check_db_connection(db_params, retry=retry - 1)
    else:
        con.close()
