import mysql.connector

class MyBankDB:
    """
    class MyBankDB is created to interact with mysql bank database 
    """
    def __init__(self) -> None:
        try:
         self._conn = mysql.connector.connect(user="root",password="dev123",host='localhost',port='3306',database='mybank_db')
         self._cursor = self._conn.cursor()

        except Exception as error:
            print("Error while connecting to database for job tracker", error)

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor    

    def execute(self, sql, params=None):
        """Implements execute function"""
        self.cursor.execute(sql, params or ())

    def commit(self):
        """Implements commit function"""
        self.connection.commit()
    
    def fetchall(self):
        """Implements fetchall function"""
        return self.cursor.fetchall()

    def fetchone(self):
        """Implement fetchone function"""
        return self.cursor.fetchone()

    def close(self, commit=True):
        """Implement close function"""
        if commit:
            self.commit()
        self.connection.close()

if __name__ == '__main__':
    my_bank_db=MyBankDB()
