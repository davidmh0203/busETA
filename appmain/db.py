import os
import pymysql
from pymysqlpool.pool import Pool

MYSQL_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "pyBook"),
    "cursorclass": pymysql.cursors.Cursor,
    "autocommit": True,
}

# Initialize a connection pool for reusing connections across requests
pool = Pool(**MYSQL_CONFIG)
pool.init()


def get_connection():
    """Return a pooled MySQL connection."""
    return pool.get_conn()
