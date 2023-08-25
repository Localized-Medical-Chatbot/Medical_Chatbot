# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

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

# set your details here
DATABASE_NAME = 'hospitaldb'
USERNAME = 'root'
PASSWORD = 'GSsql2022' # set your password 
HOST = 'localhost'


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
    
class ActionGetDoctorName(Action):

    def name(self) -> Text:
        return "action_get_doctor_name"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        db = DatabaseConnection(HOST, DATABASE_NAME, USERNAME, PASSWORD)
        results = db.query("SELECT first_name FROM doctor WHERE first_name = 'Jennifer';")
        # developer_name = results[0]
        results = str(results[0])
        db.disconnect()
        
        dispatcher.utter_message(text=results+"Just hardcorded value")
        return[]
    
class ActionGetClinicDetails(Action):

    def name(self) -> Text:
        return "action_get_clinic_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        db = DatabaseConnection(HOST, DATABASE_NAME, USERNAME, PASSWORD)
        results = db.query("SELECT last_name FROM doctor WHERE first_name = 'Jennifer';")
        results = str(results[0])
        db.disconnect()
        
        dispatcher.utter_message(text=results+"Just hardcorded value")
        return[]
