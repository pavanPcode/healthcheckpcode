import configparser
import pyodbc

# MSSQL database name
dbname = 'rcalerts_Prod'

class MSSQLHelper:
    CONFIG_PATH = 'dbConfig.ini'

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_PATH)
        self.dbinfo = {
            "server": config.get(dbname, "server"),  # MSSQL server name
            "database": config.get(dbname, "database"),
            "user": config.get(dbname, "user"),
            "password": config.get(dbname, "password"),
            "driver": "{ODBC Driver 17 for SQL Server}"  # Adjust the driver based on your setup
        }

    def dbconnect(self):
        try:
            conn_str = (
                f"DRIVER={self.dbinfo['driver']};"
                f"SERVER={self.dbinfo['server']};"
                f"DATABASE={self.dbinfo['database']};"
                f"UID={self.dbinfo['user']};"
                f"PWD={self.dbinfo['password']};"
            )
            self.dbconn = pyodbc.connect(conn_str)
            return self.dbconn.cursor()
        except pyodbc.Error as err:
            print(f"Error connecting to MSSQL Server: {err}")
            return None

    def disconnect(self):
        if hasattr(self, 'dbconn') and self.dbconn:
            self.dbconn.close()

    def queryall(self, sqlqry):
        try:
            cursor = self.dbconnect()
            if cursor:
                cursor.execute(sqlqry)
                columns = [column[0] for column in cursor.description]
                result = cursor.fetchall()
                self.disconnect()
                if len(result) == 0:
                    return {"Status": False, "ResultData": [], "Message": 'No Record Found'}
                return {"Status": True, "ResultData": result, "Message": None}
            else:
                return {"Status": False, "ResultData": [], "Message": 'Something Wrong with connection'}
        except Exception as e:
            self.disconnect()
            return {"Status": False, "ResultData": [], "Message": str(e)}

    def update(self, sqlqry):
        try:
            cursor = self.dbconnect()
            if cursor:
                cursor.execute(sqlqry)
                self.dbconn.commit()
                self.disconnect()
                return {"Status": True, "ResultData": [], "Message": None}
            else:
                return {"Status": False, "ResultData": [], "Message": 'Something Wrong with connection'}
        except Exception as e:
            self.disconnect()
            return {"Status": False, "ResultData": [], "Message": str(e)}
