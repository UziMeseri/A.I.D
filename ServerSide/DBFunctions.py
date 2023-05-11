import os
import SQLite3


class DB():
    def HashPass(self,Pass):
        '''Function receives a string which contains the entered password and hashes it'''
        import hashlib
        hash_md5 = hashlib.md5(Pass)  # make hash MD5 to  string
        return hash_md5.hexdigest()

    def __init__(self):
        self.connection = SQLite3.connect_sqlite3("Admins.db")  # connection

        def Create():
            '''Function creates a database which contains usernames and passwords'''
            self.sql = """ CREATE TABLE IF NOT EXISTS Admins(id INT,username TEXT,password TEXT);"""
            self.SQLite3.db_change(self.connection, self.sql)

            self.sql = f"""INSERT INTO Admins VALUES (100,"Police","{DB.HashPass(self,"Police100".encode())}");"""
            self.SQLite3.db_change(self.connection, self.sql)

            self.sql = f"""INSERT INTO Admins VALUES (101,"MDA","{DB.HashPass(self,"MDA101".encode())}");"""
            self.SQLite3.db_change(self.connection, self.sql)

            self.sql = f"""INSERT INTO Admins VALUES (102,"Fire","{DB.HashPass(self,"Fire102".encode())}");"""
            self.SQLite3.db_change(self.connection, self.sql)

            self.sql = f"""INSERT INTO Admins VALUES (1,"Admin","{DB.HashPass(self,"Password".encode())}");"""
            self.SQLite3.db_change(self.connection, self.sql)

            self.sql = f"""INSERT INTO Admins VALUES (2,"1","{DB.HashPass(self,"1".encode())}");"""
            self.SQLite3.db_change(self.connection, self.sql)


    def CheckLogin(self,User,Pass):
        '''Function receives a username and password and checks if those exist in the database, returns True if exists, False otherwise'''
        print("checking...")
        sql = """SELECT * FROM Admins"""
        Rows = SQLite3.db_query(self.connection, sql)

        for Details in Rows:
            if User == Details[1] and Pass == Details[2]:
                return True
        return False







