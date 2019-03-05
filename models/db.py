# Savital https://github.com/Savital

import sqlite3

class Users():
    createTableSQL = "CREATE TABLE IF NOT EXISTS users(username CHAR)"
    dropTableSQL = "DROP TABLE IF EXISTS users"
    selectSQL = "SELECT * FROM users"
    selectByNameSQL = "SELECT * FROM users WHERE username='{0}'"
    insertSQL = "INSERT INTO users VALUES ('{0}')"
    deleteSQL = "DELETE FROM users WHERE username = '{0}'"

    def __init__(self):
        super(Users, self).__init__()
        self.construct()

    def construct(self):
        pass

    def createTable(self):
        self.conn = sqlite3.connect("keypadMonitoringDB.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.createTableSQL)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def dropTable(self):
        self.conn = sqlite3.connect("keypadMonitoringDB.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.dropTableSQL)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def select(self):
        self.conn = sqlite3.connect("keypadMonitoringDB.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.selectSQL)
        results = self.cursor.fetchall()
        self.cursor.close()
        self.conn.close()
        return results

    def selectByName(self, name):
        self.conn = sqlite3.connect("keypadMonitoringDB.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.selectByNameSQL.format(name))
        results = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return results

    def insert(self, name):
        self.conn = sqlite3.connect("keypadMonitoringDB.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.insertSQL.format(name))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def delete(self, name):
        self.conn = sqlite3.connect("keypadMonitoringDB.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.deleteSQL.format(name))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

class Log():
    createTableSQL = "CREATE TABLE IF NOT EXISTS log(username CHAR, id INT, state INT, layout INT, scancode INT, downtime INT, searchtime INT, keyname CHAR)"
    dropTableSQL = "DROP TABLE IF EXISTS log"
    selectSQL = "SELECT * FROM log"
    selectByNameSQL = "SELECT * FROM log WHERE username='{0}'"
    insertSQL = "INSERT INTO log VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')" #TODO UNRECOGNIZED TOKEN "''')"
    deleteSQL = "DELETE FROM log WHERE username = '{0}'"

    def __init__(self):
        super(Log, self).__init__()
        self.construct()

    def construct(self):
        pass

    def createTable(self):
        self.conn = sqlite3.connect("keypadMonitoringDB.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.createTableSQL)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def dropTable(self):
        self.conn = sqlite3.connect("keypadMonitoringDB.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.dropTableSQL)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def select(self):
        self.conn = sqlite3.connect("keypadMonitoringDB.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.selectSQL)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def selectByName(self, name):
        self.conn = sqlite3.connect("keypadMonitoringDB.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.selectByNameSQL.format(name))
        results = self.cursor.fetchall()
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return results

    def insert(self, name, list):
        self.conn = sqlite3.connect("keypadMonitoringDB.db")
        self.cursor = self.conn.cursor()
        if len(list) == 0:
            pass
        elif len(list[0]) == 1:
            self.cursor.execute(self.insertSQL.format(name, list[0], list[1], list[2], list[3], list[4], list[5], list[6]))
        else:
            for item in list:
                self.cursor.execute(self.insertSQL.format(name, item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def delete(self, name):
        self.conn = sqlite3.connect("keypadMonitoringDB.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.deleteSQL.format(name))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

