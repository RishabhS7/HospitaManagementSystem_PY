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
