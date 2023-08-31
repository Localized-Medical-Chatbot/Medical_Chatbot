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
    
    def insert(self, query):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        self.connection.commit()
        self.cursor.close()
        return True
    
# set your details here
DATABASE_NAME = 'hospitaldb'
USERNAME = 'root'
PASSWORD = 'GSsql2022' # set your password 
HOST = 'localhost'
    
    
first_name = "Suwan"
last_name = "Sankaja"
date = "2023-08-31"
doctor_id = 5
start_time = '10:00:00'
end_time = '10:30:00'

AppointmentQuarry = f"""
            INSERT INTO `appointment` (`doctor_id`, `first_name`, `last_name`, `start_time`, `end_time`, `date`) VALUES
            ({doctor_id}, '{first_name}', '{last_name}', '{start_time}', '{end_time}', '{date}');
        """
db = DatabaseConnection(HOST, DATABASE_NAME, USERNAME, PASSWORD)
success = db.insert(AppointmentQuarry)
db.disconnect() 
print(success)