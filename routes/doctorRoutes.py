from flask import Blueprint, request, jsonify
from models.doctor import Doctor,Doctor_Appointments
from models.patient import ContactInformation,Patient_Appointment
from flask_pymongo import ObjectId
import json
from configs.app import db

doctor_blueprint = Blueprint('doctor', __name__)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o) 
# route to add a new doctor
@doctor_blueprint.route('/addDoctor',methods=['POST'])
def add_Doctor():
    data = request.get_json()
    if not data.get('name') or not data.get('specialization'):
        return jsonify({'error': 'Missing name, specialization'}), 400

    existing_doctor = db.doctors.find_one({'contact_information.email': data.get('email')})
    if existing_doctor:
        return jsonify({'error': 'Email already registered'}), 400
    
    contact_info = ContactInformation(phone=data['contact_information']['phone'], email=data['contact_information']['email'], address=data['contact_information']['address'],).to_dict()
    doctor = Doctor(name=data['name'], specialization=data['specialization'], contact_information=contact_info,start_time=data['start_time'],total_shift_time=data['total_shift_time'],break_start_time=data['break_start_time'], appointments_schedule={})
    db.doctors.insert_one(vars(doctor))
    return jsonify({'message': 'Doctor registered successfully'}), 201


# Define the route to get a doctor by ID
@doctor_blueprint.route('/doctors/<doctor_id>', methods=['GET'])
def get_doctor_by_id(doctor_id):
    doctor = db.doctors.find_one_or_404({'_id': ObjectId(doctor_id)})
    return JSONEncoder().encode(doctor)

# Define the route to update a patient
@doctor_blueprint.route('/updateDoctor/<doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    # Get the patient from the database
    doctor_collection = db.doctors
    doctor = doctor_collection.find_one({'_id': ObjectId(doctor_id)})

    if not doctor:
        return jsonify({"error": "doctor not found"}), 404

    data = request.get_json()
    doctor_data = {
        'name': data.get('name', doctor['name']),
        'age': data.get('age', doctor['age']),
        'gender': data.get('gender', doctor['gender']),
        'start_time': data.get('start_time',doctor['start_time']),
        'total_shift_time' : data.get('total_shift_time',doctor['total_shift_time']),
        'break_start_time' : data.get('break_start_time',doctor['break_start_time']),
        'contact_information': data.get('contact_information', doctor['contact_information']),
        
    }

    doctor_collection.update_one({'_id': ObjectId(doctor_id)}, {'$set': doctor_data})

    return jsonify({"message": "doctor information updated successfully"}), 200    

# Define the route to update a patient
@doctor_blueprint.route('/addAppointment', methods=['POST'])
def add_appointment():
    data = request.get_json()
    doctor_id = data.get('doctor_id')
    patient_id = data.get('patient_id')
    date = data.get('date')
    time = data.get('time')
    duration_in_minutes = data.get('duration_in_minutes')
    department = data.get('department')

    if not doctor_id or not patient_id or not date or not time or not duration_in_minutes:
     return jsonify({"error": " invalid details"}), 404
    
    patients_collection = db.patients
    patient = patients_collection.find_one({'_id': ObjectId(patient_id)})
    doctors_collection = db.doctors
    doctor = doctors_collection.find_one({'_id':ObjectId(doctor_id)})

    if not patient or not doctor:
        return jsonify({"error": "Patient or doctor not found"}), 404

    doctor_appointment_data = Doctor_Appointments(patient_id=patient_id,date=date,time=time,duration_in_minutes=duration_in_minutes)
    patient_appointment_data = Patient_Appointment(doctor_id=doctor_id,date=date,time=time,duration_in_minutes=duration_in_minutes,department=department)
            # Add appointment to doctor's schedule
    db.doctors.update_one(
            {'_id': doctor_id},
            {'$push': {'appointments_schedule.' + date: doctor_appointment_data}}
        )
    db.patients.update_one(
        {'_id':patient_id},
        {'$push':{'appointment_records':patient_appointment_data}}
    )
    return jsonify({'message': 'Appointment registered successfully'}), 201
