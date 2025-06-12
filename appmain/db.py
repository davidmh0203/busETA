import os
import pymysql
from dbutils.pooled_db import PooledDB

POOL = PooledDB(
    creator=pymysql,
    maxconnections=5,
    blocking=True,
    host=os.environ.get('DB_HOST'),
    port=int(os.environ.get('DB_PORT', 3306)),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_NAME'),
    cursorclass=pymysql.cursors.DictCursor
)

def get_connection():
    return POOL.connection()
