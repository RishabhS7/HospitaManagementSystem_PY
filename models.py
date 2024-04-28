from flask_pymongo import PyMongo

mongo = PyMongo()

class User:
    def __init__(self, username, password, level, is_del=False):
        self.username = username
        self.password = password
        self.level = level
        self.is_del = is_del

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'level': self.level,
            'is_del': self.is_del
        }

# Schema for Appointment Records
class Patient_Appointment:
    def __init__(self, doctor_id, time, duration_in_minutes, department, status,date):
        self.doctor_id = doctor_id
        self.time = time
        self.date = date
        self.duration_in_minutes = duration_in_minutes
        self.department = department
        self.status = status
    def to_dict(self):
        return {
            'doctor_id':self.doctor_id,
            'time':self.time,
            'duration_in_minutes':self.duration_in_minutes,
            'department':self.department,
            'status':self.status,
            'date':self.date
        }        
    
class MedicalHistory:
    def __init__(self, previous_diagnoses=[], allergies=[], medications=[]):
        self.previous_diagnoses = previous_diagnoses
        self.allergies = allergies
        self.medications = medications    
    def to_dict(self):
        return {
            'previous_diagnoses': self.previous_diagnoses,
            'allergies': self.allergies,
            'medications': self.medications
        }    

class ContactInformation:
    def __init__(self, phone, email, address):
        self.phone = phone
        self.email = email
        self.address = address   
    def to_dict(self):
        return {
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }    

# Define the schema for the patient collection
class Patient:
    def __init__(self, name, age, gender, contact_information, medical_history, appointment_records=[]):
        self.name = name
        self.age = age
        self.gender = gender
        self.contact_information = contact_information
        self.medical_history = medical_history
        self.appointment_records = appointment_records

#Appointments schedule
class Doctor_Appointments:
    def __init__(self, patient_id, date, time, duration_in_minutes):
        self.patientId = patient_id
        self.date = date
        self.time = time
        self.duration_in_minutes = duration_in_minutes

    def to_dict(self):
        return {
            'patient_id': self.patient_id,
            'date': self.date,
            'time': self.time,
            'duration_in_minutes':self.duration_in_minutes
        }

# Define the schema for the patient collection
class Doctor:
    def __init__(self, name, specialization, contact_information,start_time,total_shift_time ,break_start_time,appointments_schedule={}):
        self.name = name
        self.specialization = specialization
        self.contact_information = contact_information
        self.start_time = start_time
        self.total_shift_time = total_shift_time  
        self.break_start_time = break_start_time 
        self.appointments_schedule = appointments_schedule


# Define the schema for the patient collection
class Department:
    def __init__(self, name, services=[], doctors_assigned=[]):
        self.name = name
        self.services = services
        self.doctors_assigned = doctors_assigned