import sqlite3

def connect_sqlite3(dbname):
    connection = sqlite3.connect(dbname)
    return connection

def db_change(connection,sql):
    cursor = connection.cursor()
    cursor.execute(sql) # execute the SQl command
    connection.commit() #DO the command
    print( "SQL executed succesfully")

def db_query(connection,sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows