from flask import Blueprint, request, jsonify
from configs.app import db
from models.patient import Patient, ContactInformation, MedicalHistory
from flask_pymongo import ObjectId
import json

patient_blueprint = Blueprint('patient', __name__)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o) 
    
#Route to add patient
@patient_blueprint.route('/addPatient',methods=['POST'])
def add_patient():
    data = request.get_json()
    if not data.get('name') or not data.get('age') or not data.get('gender'):
        return jsonify({'error': 'Missing username, email, or password'}), 400


    print("db data",data)
    existing_patient = db.patients.find_one({'contact_information.email': data.get('email')})
    if existing_patient:
        return jsonify({'error': 'Email already registered'}), 400
    
    medical_history = MedicalHistory(previous_diagnoses=[], allergies=[], medications=[]).to_dict()
    contact_info = ContactInformation(phone=data['contact_information']['phone'], email=data['contact_information']['email'], address=data['contact_information']['address'],).to_dict()
    patient = Patient(name=data['name'], age=data['age'], gender=data['gender'], contact_information=contact_info, medical_history=medical_history, appointment_records=[])
    db.patients.insert_one(vars(patient))
    return jsonify({'message': 'User registered successfully'}), 201

# Define the route to get a patient by ID
@patient_blueprint.route('/patients/<string:patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    # patient_id = request.args.get('patient_id')  
    print("here")
    patient = db.patients.find_one({'_id': ObjectId(patient_id)})
    return JSONEncoder().encode(patient)

# Define the route to update a patient
@patient_blueprint.route('/updatePatient/<patient_id>', methods=['PUT'])
def update_patient(patient_id):
    # Get the patient from the database
    patients_collection = db.patients
    patient = patients_collection.find_one({'_id': ObjectId(patient_id)})

    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    data = request.get_json()
    medical_history = data.get('medical_history')
    patient_data = {
        'name': data.get('name', patient['name']),
        'age': data.get('age', patient['age']),
        'gender': data.get('gender', patient['gender']),
        'contact_information': data.get('contact_information', patient['contact_information']),
        'medical_history': {
            'previous_diagnoses': medical_history.get('previous_diagnoses', patient['medical_history']['previous_diagnoses']),
            'allergies': medical_history.get('allergies', patient['medical_history']['allergies']),
            'medications': medical_history.get('medications', patient['medical_history']['medications'])
        }
    }

    patients_collection.update_one({'_id': ObjectId(patient_id)}, {'$set': patient_data})

    return jsonify({"message": "Patient information updated successfully"}), 200    