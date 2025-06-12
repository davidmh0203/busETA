import pymysql
from dbutils.pooled_db import PooledDB
from pymysql import cursors


POOL = PooledDB(
    creator=pymysql,
    maxconnections=5,
    blocking=True,
    host='localhost',
    user='root',
    password='12341234',
    database='bus_eta',
    cursorclass=pymysql.cursors.DictCursor
)

def get_connection():
    return POOL.connection()
