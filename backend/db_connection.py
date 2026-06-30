import pymysql
import pymysql.cursors
import os
from dbutils.pooled_db import PooledDB

pool = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=5,
    blocking=True,
    host=os.getenv("DB_HOST", "db"),
    port=int(os.getenv("DB_PORT", "3306")),
    db=os.getenv("DB_NAME", "gpclinic"),
    user=os.getenv("DB_USER", "gpclinic_user"),
    password=os.getenv("DB_PASSWORD", "gpclinic_pass"),
    cursorclass=pymysql.cursors.DictCursor,
)


def get_db():
    return pool.connection()