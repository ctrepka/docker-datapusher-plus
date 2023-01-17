import os
import sys

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, AsIs
from sqlalchemy import create_engine

TEST = os.environ.get("TEST", "DEFAULT ENV VALUE")
VENV = os.environ.get("VENV", "/")

# db host
db_host = os.environ.get("DB_HOST", "")
# Designed/intended for use with mdillon:11 postgis image.
# See https://hub.docker.com/r/mdillon/postgis/
# for notes on default environment variable settings,
# which are taken into account below.
# the configuration should, however, work for most postgres images.
master_user = os.environ.get("POSTGRES_USER", "postgres")
master_passwd = os.environ.get("POSTGRES_PASSWORD")
master_database = os.environ.get("POSTGRES_DB", master_user)
# creds for datapusher-plus jobs db
dpp_jobs_user = os.environ.get("JOBS_DB_USER", "jobs")
dpp_jobs_passwd = os.environ.get("JOBS_DB_PASSWORD", "jobsPasswd")
dpp_jobs_database = os.environ.get("JOBS_DB_NAME", "jobs")

os.system("echo db: {} user: {} passwd: {}".format(
    dpp_jobs_database,
    dpp_jobs_user,
    dpp_jobs_passwd
))


class DB_Params:
    def __init__(self, conn_str):
        self.db_user = conn_str.url.username
        self.db_passwd = conn_str.url.password
        self.db_host = conn_str.url.host
        self.db_name = conn_str.url.database


def check_db_connection(db_params, retry=None):

    os.system('echo Checking whether database is up...')

    if retry is None:
        retry = 20
    elif retry == 0:
        print('Giving up...')
        sys.exit(1)

    try:
        con = psycopg2.connect(user=master_user,
                               host=db_host,
                               password=master_passwd,
                               database=master_database)

    except psycopg2.Error as e:
        print((str(e)))
        os.system(
            "echo 'unable to connect. trying again in 30 seconds {}'".format(e))
        print('Unable to connect to the database...try again in a while.')

        import time
        time.sleep(10)
        check_db_connection(db_params=db_params, retry=retry - 1)

    else:
        os.system('echo "Database is up..."')
        con.close()


def create_user(db_params):
    con = None

    try:
        con = psycopg2.connect(user=master_user,
                               host=db_params.db_host,
                               password=master_passwd,
                               database=master_database)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        print("Creating user {}".format(db_params.db_user.split("@")[0]))
        cur.execute("CREATE ROLE {} WITH LOGIN NOSUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION PASSWORD '{}'".format(
            AsIs(db_params.db_user.split("@")[0]),
            db_params.db_passwd,
        ))
    except(Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
    finally:
        cur.close()
        con.close()

    try:
        con = psycopg2.connect(user=master_user,
                               host=db_params.db_host,
                               password=master_passwd,
                               database=master_database)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        print("Changing password of user {}".format(
            db_params.db_user.split("@")[0]))
        # If password pulled from aws secrets, it may have changed.
        # This operation may duplicate a portion of the above command, but ensured the RDS credentials for the role
        # Are synchronized with the secrets in aws secrets manager
        cur.execute("ALTER ROLE {} PASSWORD '{}'".format(
            AsIs(db_params.db_user.split("@")[0]),
            db_params.db_passwd,
        ))
    except(Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
    finally:
        cur.close()
        con.close()


def create_db(db_params):
    con = None
    try:
        con = psycopg2.connect(user=master_user,
                               host=db_params.db_host,
                               password=master_passwd,
                               database=master_database)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute('GRANT "' + db_params.db_user.split("@")
                    [0] + '" TO "' + master_user.split("@")[0] + '"')
        print("Creating database " + db_params.db_name + " with owner " +
              db_params.db_user.split("@")[0])
        cur.execute('CREATE DATABASE ' + db_params.db_name +
                    ' OWNER "' + db_params.db_user.split("@")[0] + '"')
        cur.execute('GRANT ALL PRIVILEGES ON DATABASE ' + db_params.db_name +
                    ' TO "' + db_params.db_user.split("@")[0] + '"')
        if is_pg_buffercache_enabled(db_params) >= 1:
            # FIXME: This is a known issue with pg_buffercache access
            # For more info check this thread:
            # https://www.postgresql.org/message-id/21009351582737086%40iva6-22e79380f52c.qloud-c.yandex.net
            print("Granting privileges on pg_monitor to " +
                  db_params.db_user.split("@")[0])
            cur.execute('GRANT "pg_monitor" TO "' +
                        db_params.db_user.split("@")[0] + '"')
    except(Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
    finally:
        cur.close()
        con.close()


def is_pg_buffercache_enabled(db_params):
    con = None
    result = None
    try:
        con = psycopg2.connect(user=master_user,
                               host=db_params.db_host,
                               password=master_passwd,
                               database=db_params.db_name)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute("SELECT count(*) FROM pg_extension " +
                    "WHERE extname = 'pg_buffercache'")
        result = cur.fetchone()
    except(Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
    finally:
        cur.close()
        con.close()
    return result[0]


# Create master db connection string
master_engine = create_engine('postgresql+psycopg2://{u}:{p}@{h}/{db}'.format(
    u=master_user,
    p=master_passwd,
    h=db_host,
    db=master_database
))

# Create master db connection params
db_params = DB_Params(master_engine)
# Check connection to master db
check_db_connection(db_params=db_params)


# Create datapusher-plus jobs db connection string
dpp_jobs_engine = create_engine('postgresql+psycopg2://{u}:{p}@{h}/{db}'.format(
    u=dpp_jobs_user,
    p=dpp_jobs_passwd,
    h=db_host,
    db=dpp_jobs_database
))
# Create datapusher-plus jobs db connection params
dpp_jobs_params = DB_Params(dpp_jobs_engine)
# Create user for datapusher-plus jobs db
try:
    create_user(dpp_jobs_params)
except(Exception, psycopg2.DatabaseError) as error:
    os.system("echo {}".format(error))
# Create datapusher-plus jobs db and grant perms to user
try:
    create_db(dpp_jobs_params)
except(Exception, psycopg2.DatabaseError) as error:
    os.system("echo {}".format(error))
