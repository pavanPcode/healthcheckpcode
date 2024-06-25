import configparser
import mysql.connector
#Faqs_Apis
dbname = 'HealthCheck_Prod'

class MySQLHelper:
    CONFIG_PATH = 'dbConfig.ini'

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_PATH)
        self.dbinfo = {
            "host": config.get(dbname, "host"),
            "database": config.get(dbname, "database"),
            "user": config.get(dbname, "user"),
            "password": config.get(dbname, "password"),
        }

    def dbconnect(self):
        try:
            self.dbconn = mysql.connector.connect(**self.dbinfo)
            return self.dbconn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL Server: {err}")
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


