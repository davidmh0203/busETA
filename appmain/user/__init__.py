import pymysql
from appmain.db import get_connection

# Create users table if it does not exist
conn = get_connection()
cursor = conn.cursor()

SQL = (
    "CREATE TABLE IF NOT EXISTS users ("
    "id INT AUTO_INCREMENT PRIMARY KEY,"
    " username VARCHAR(255) NOT NULL,"
    " email VARCHAR(255) NOT NULL,"
    " passwd VARBINARY(255) NOT NULL,"
    " authkey VARCHAR(255)"
    ")"
)

cursor.execute(SQL)
conn.commit()
cursor.close()
conn.close()
