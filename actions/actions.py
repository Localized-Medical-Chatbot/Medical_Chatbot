# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from datetime import datetime, timedelta

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from datetime import timedelta, date
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
import mysql.connector
from rasa_sdk.events import UserUttered
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
        
        GetAllDoctorsQuerry = f"""SELECT
                                    d.first_name,
                                    d.last_name,
                                    s.type AS specialization,
                                    d.id
                                FROM
                                    doctor AS d
                                JOIN
                                    speciality AS s ON d.specialty = s.id"""
        
        db = DatabaseConnection(HOST, DATABASE_NAME, USERNAME, PASSWORD)
        all_doctors = db.query(GetAllDoctorsQuerry)
        db.disconnect()

        doctor_names = []
        for row in all_doctors:
            doctor_names.extend(row)
        # # doctor_names = [item.lower() for item in doctor_names]
        # doctor_names = [item.lower() if isinstance(item, str) else item for item in doctor_names]

        string =  ' These are few Doctors that we have: \n\n **** '
        for row in all_doctors:
            full_name = f"{row[0]} {row[1]}"
            specialization = row[2]
            string += f"{full_name} : {specialization}. **** \n"
        dispatcher.utter_message(text=string)
        return[]
    
class ActionGetClinicDetails(Action):

    def name(self) -> Text:
        return "action_get_clinic_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        clinic_type = tracker.get_slot("clinic_type")
        if not clinic_type:
            dispatcher.utter_message(text="Please provide the name of the clinic that you want to know more about.")
        else:
            clinic_types = ["pediatric","psychology","burn","cardiology","gynecology","neurology","surgery"]
            if clinic_type not in clinic_types:
                dispatcher.utter_message(text=f"We dont have clinic that you specified. we have {clinic_types}. please provide one of them as clinic type you want. ")
            else:
                db = DatabaseConnection(HOST, DATABASE_NAME, USERNAME, PASSWORD)
                results = db.query(f"SELECT description FROM clinic WHERE name = '{clinic_type}';")
                response= f"Details of the {clinic_type} clinic\n\n"
                db.disconnect()

                for row in results:
                    description = str(row[0])
                    response = f"{response} {description} \n\n"

                dispatcher.utter_message(text= response)
        return[]


class ActionGetAdditionalClinicDetails(Action):

    def name(self) -> Text:
        return "action_get_additional_clinic_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        clinic_type = tracker.get_slot("clinic_type")
        if not clinic_type:
            dispatcher.utter_message(text="Please provide the name of the clinic that you want to know more about.")
        else:
            clinic_types = ["pediatric","psychology","burn","cardiology","gynecology","neurology","surgery"]
            if clinic_type not in clinic_types:
                dispatcher.utter_message(text=f"We dont have clinic that you specified. we have {clinic_types}. please provide one of them as clinic type you want. ")
            else:
                db = DatabaseConnection(HOST, DATABASE_NAME, USERNAME, PASSWORD)
                results = db.query(f"SELECT start_time, end_time, date FROM schedule WHERE clinic_id = ( SELECT id FROM clinic WHERE name = '{clinic_type}');")
                response= f"{clinic_type} Clinic: The schedule of the clinic is as follows.\n\n"
                db.disconnect()

                for row in results:
                    start_time = timedelta(seconds=row[0].seconds)
                    end_time = timedelta(seconds=row[1].seconds)
                    date_value = row[2]

                    start_time_str = str(start_time.seconds // 3600).zfill(2) + ':' + str((start_time.seconds // 60) % 60).zfill(2)
                    end_time_str = str(end_time.seconds // 3600).zfill(2) + ':' + str((end_time.seconds // 60) % 60).zfill(2)
                    date_str = date_value.strftime('%Y-%m-%d')

                    response = f"{response} ආරම්භක වෙලාව: {start_time_str}\n    අවසාන වන වෙලාව: {end_time_str}\n    දිනය:{date_str} \n\n"

                dispatcher.utter_message(text= response)
                

        return[]


class ValidateAppointmentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_appointment_form"
    
    def validate_doctor_name(
            self,
            slot_value: any,
            dispatcher: CollectingDispatcher,
            tarcker: Tracker,
            domain: DomainDict) -> Dict[Text,Any]:
        
        
        GetAllDoctorsQuerry = f"""SELECT
                                    d.first_name,
                                    d.last_name,
                                    s.type AS specialization,
                                    d.id
                                FROM
                                    doctor AS d
                                JOIN
                                    speciality AS s ON d.specialty = s.id"""
        
        db = DatabaseConnection(HOST, DATABASE_NAME, USERNAME, PASSWORD)
        all_doctors = db.query(GetAllDoctorsQuerry)
        db.disconnect()

        doctor_names = []
        for row in all_doctors:
            doctor_names.extend(row)
        # doctor_names = [item.lower() for item in doctor_names]
        doctor_names = [item.lower() if isinstance(item, str) else item for item in doctor_names]


        if not slot_value.lower() in doctor_names:
            message = "You entered Docter name is not in our database. Please provide doctors in our hospital \n\n"
            buttons = []
            for row in all_doctors:
                full_name = f"{row[0]} {row[1]}"
                specialization = row[2]
                title = f"{full_name} : {specialization}. \n ***"
                message += title
                # payload = f'/get_doctor_name_frm_payload{{"doctor_name":"{row[0]}"}}'
                # payload = f'/get_doctor_name_frm_payload{{"doctor_name":"{row[0]}"}}'
                # buttons.append({"title":title, "payload":payload})
                # message += f"{full_name} : {specialization}\n"

            dispatcher.utter_message(text= message)
            return {"doctor_name": None}
        
        else:
            GetDoctorId = f"""SELECT
                            d.id
                        FROM
                            doctor AS d
                        JOIN
                            speciality AS s ON d.specialty = s.id
                        WHERE
                            CONCAT(d.first_name, ' ', d.last_name) LIKE '%%{slot_value.lower()}%%'
                            OR d.first_name LIKE '%%{slot_value.lower()}%%'
                            OR d.last_name LIKE '%%{slot_value.lower()}%%';"""
            db = DatabaseConnection(HOST, DATABASE_NAME, USERNAME, PASSWORD)
            doctor_id = db.query(GetDoctorId)
            db.disconnect()       # ----------------
            doctor_id = str(doctor_id[0][0])
            return{"doctor_id": doctor_id}
    
    # def doctor_name_frm_entity(
    #         self,
    #         slot_value: any,
    #         dispatcher: CollectingDispatcher,
    #         tarcker: Tracker,
    #         domain: DomainDict) -> Dict[Text,Any]:
        
    #     GetDoctorId = f"""SELECT
    #                         d.id,d.first_name
    #                     FROM
    #                         doctor AS d
    #                     JOIN
    #                         speciality AS s ON d.specialty = s.id
    #                     WHERE
    #                         CONCAT(d.first_name, ' ', d.last_name) LIKE '%%{slot_value.lower()}%%'
    #                         OR d.first_name LIKE '%%{slot_value.lower()}%%'
    #                         OR d.last_name LIKE '%%{slot_value.lower()}%%';"""
    #     db = DatabaseConnection(HOST, DATABASE_NAME, USERNAME, PASSWORD)
    #     doctor_details = db.query(GetDoctorId)
    #     db.disconnect()       # ----------------
    #     doctor_id = str(doctor_details[0][0])
    #     doctor_name = str(doctor_details[0][1]) 
    #     return{"doctor_name":doctor_name,"doctor_id": doctor_id}
          
    
    def validate_date(
            self,
            slot_value: any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> Dict[Text,Any]:
        
        date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']

        # Try parsing the date using each format
        for date_format in date_formats:
            try:
                date_obj = datetime.strptime(slot_value, date_format)
                break  # Stop if successfully parsed
            except ValueError:
                pass

        # Get today's date
        today = datetime.now().date()

        # Calculate the date one month from now
        next_month = today + timedelta(days=30)

        # Check if the parsed date is within today and the next month
        if today <= date_obj.date() <= next_month:
            doc_id = int(tracker.get_slot("doctor_id"))
            app_date = str(tracker.get_slot("date"))
            print(doc_id,app_date)

            AvilabilityTimeQuarry = f"""SELECT start_time, end_time FROM 
                                        availability WHERE doctor_id = {doc_id} AND date = '{app_date}';"""
            db = DatabaseConnection(HOST, DATABASE_NAME, USERNAME, PASSWORD)
            avilable_times = db.query(AvilabilityTimeQuarry)
            db.disconnect()
            print(avilable_times)
            message = ""
            if len(avilable_times):
                message = "You can meet your Doctor:  \n"
                buttons=[]
                for row in avilable_times:
                    start_time = row[0]
                    end_time = row[1]
                    title = f"- {app_date} from {start_time} to {end_time}.\n"
                    payload = f'/time_slot{{"start_time":"{start_time}", "end_time":"{end_time}"}}'
                    buttons.append({"title":title, "payload":payload})
                
                dispatcher.utter_message(text=message,buttons=buttons)
                return {"date":slot_value}
            else:
                AvilabilityQuarry = f"""SELECT date, start_time, end_time FROM 
                                    availability WHERE doctor_id = {doc_id} AND date BETWEEN '{today}' AND '{next_month}';"""
                db = DatabaseConnection(HOST, DATABASE_NAME, USERNAME, PASSWORD)
                avilable_dates = db.query(AvilabilityQuarry)
                db.disconnect()
                message = f"The doctor is not available on {app_date}. Please provide a date from available dates:  \n\n"
                buttons = []
                for row in avilable_dates:
                    avilable_dt = row[0]
                    start_time = row[1]
                    end_time = row[2]
                    title = f"- {avilable_dt} from {start_time} to {end_time}.\n"
                    payload = f'/time_slot{{"date":"{avilable_dt}","start_time": "{start_time}", "end_time": "{end_time}"}}'
                    buttons.append({"title":title, "payload":payload})

                dispatcher.utter_message(text=message,buttons=buttons)
                return {"date":None}
        else:
            message = "Sorry You can only create an appointment within a month from today. the date you enterd is not valid. \n"
            dispatcher.utter_message(text= message)
            return {"date": None}


            # GetDoctorName = f"""SELECT first_name, last_name
            #                     FROM doctor
            #                     WHERE id = {int(doctor_id[0][0])};"""
            # doc_name = db.query(GetDoctorName)
            # db.disconnect()

            # return{"doctor_name": str(doc_name[0][0]+" "+doc_name[0][1])}
        

class ActionSubmitAppointment(Action):

    def name(self) -> Text:
        return "action_submit_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        first_name = tracker.get_slot("first_name")
        last_name = tracker.get_slot("last_name")
        date = tracker.get_slot("date")
        doctor_id = int(tracker.get_slot("doctor_id"))
        start_time = tracker.get_slot("start_time")
        end_time = tracker.get_slot("end_time")

        AppointmentQuarry = f"""
                    INSERT INTO `appointment` (`doctor_id`, `first_name`, `last_name`, `start_time`, `end_time`, `date`) VALUES
                    ({doctor_id}, '{first_name}', '{last_name}', '{start_time}', '{end_time}', '{date}');
                """
        db = DatabaseConnection(HOST, DATABASE_NAME, USERNAME, PASSWORD)
        success = db.insert(AppointmentQuarry)
        db.disconnect()  
        if success: 
            response = "Your appointment was successfully saved, on the database !!!  The confirmation of appointment with the doctor and The billing details will be informed to you soon."
        else: 
            response = "Sorry your appointment cannot be created!"
        dispatcher.utter_message(text= response)
                
        return[]


class ActionAuthenticateUser(Action):

    def name(self) -> Text:
        return "action_authenticate_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extracting username and password from the slots
        username = tracker.get_slot('username')
        password = tracker.get_slot('password')
        
        # Connecting to the MySQL database
        try:
            db = DatabaseConnection(HOST, DATABASE_NAME, USERNAME, PASSWORD)
            Query = f"SELECT password FROM users WHERE username='{username}'"
            result = db.query(Query)
            
            if result:
                stored_password = result[0][0]
                print(stored_password)
                if password == stored_password:
                    dispatcher.utter_message(text="Authentication successful!")
                    db.disconnect()
                else:
                    print("Incorrect")
                    dispatcher.utter_message(text="Incorrect password. Please try again.")
                    db.disconnect()
                    tracker.slots['usename'] = None
                    tracker.slots['password'] = None
                    print("incorrect 2")
                    print(tracker.getSlot("password"))

            else:
                dispatcher.utter_message(text="Username not found. Please register or try again.")
                db.disconnect()
                # return {"username": None,}
                tracker.slots['usename'] = None
                tracker.slots['password'] = None
                # evt = UserUttered("/user_login")
                # return [evt]
            return []
                  
            
        except Exception as e:
            dispatcher.utter_message(text=f"Error during authentication: {str(e)}")
        
        return []
    