import mysql.connector

class DatabaseConnection:
    hostname = None
    database = None
    username = None
    password = None
    connection = None
    cursor = None
    query = None

    def __init__(self, hostname, database, username, password):
        if not self.connection:
            self.hostname = hostname
            self.database = database
            self.username = username
            self.password = password
            self.connect()

    def connect(self):
        self.connection = mysql.connector.connect(
            host     = self.hostname,
            user     = self.username,
            password = self.password,
            database = self.database)
        
        return self.connection

    def disconnect(self):
        self.cursor.close()
        self.connection.close()
    
    def query(self, query):
        result = []

        self.cursor = self.connection.cursor()
        self.cursor.execute(query)

        for row in self.cursor:
            result.append(row)

        return result

    def count(self, table, condition = None):
        return len(self.simple_query(table, '*', condition))