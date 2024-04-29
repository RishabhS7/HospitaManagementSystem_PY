from flask import Blueprint, request, jsonify
from models.department import Department
from flask_pymongo import ObjectId
import json
from configs.app import db

department_blueprint = Blueprint('department', __name__)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o) 
# route to add a new doctor
@department_blueprint.route('/addDepartment',methods=['POST'])
def add_Department():
    data = request.get_json()
    name = data.get('name')
    services = data.get('services')
    doctors_assigned = data.get('doctors_assigned')

    if not name :
        return jsonify({'error': 'Missing name'}), 400

    existing_department = db.departments.find_one({'name': name})
    if existing_department:
        return jsonify({'error': 'department already registered'}), 400
    
    department = Department(name=name, services=services, doctors_assigned=doctors_assigned)
    db.departments.insert_one(vars(department))
    return jsonify({'message': 'Department registered successfully'}), 201

@department_blueprint.route('/addServiceToDepartment', methods=['POST'])
def add_service_to_department():
    data = request.json
    department_name = data.get('department_name')
    service = data.get('service')

    # Check if department exists
    department = db.departments.find_one({'name': department_name})
    if department:
        # Add service to department
        db.departments.update_one(
            {'name': department_name},
            {'$push': {'services': service}}
        )

        return jsonify({'message': 'Service added successfully'}), 200
    else:
        return jsonify({'error': 'Department not found'}), 404

@department_blueprint.route('/addDoctorToDepartment', methods=['POST'])
def add_doctor_to_department():
    data = request.json
    department_name = data.get('department_name')
    doctor_name = data.get('doctor_name')

    # Check if department exists
    department = db.departments.find_one({'name': department_name})
    if department:
        # Add doctor to department
        db.departments.update_one(
            {'name': department_name},
            {'$push': {'doctors_assigned': doctor_name}}
        )

        return jsonify({'message': 'Doctor added successfully'}), 200
    else:
        return jsonify({'error': 'Department not found'}), 404

   

@department_blueprint.route('/search', methods=['GET'])
def search_by_initial():
    search_type = request.args.get('type')  # Type can be 'department', 'doctor', or 'patient'
    letters = request.args.get('letters')

    if not letters or len(letters) < 2:
        return jsonify({'error': 'Initial letters should be at least 2 characters long'})

    if search_type == 'department':
        departments = db.departments.find({'name': {'$regex': '^' + letters, '$options': 'i'}})
        results = [dept for dept in departments]
    elif search_type == 'doctor':
        doctors = db.doctors.find({'name': {'$regex': '^' + letters, '$options': 'i'}})
        results = [doc for doc in doctors]
    elif search_type == 'patient':
        patients = db.patients.find({'name': {'$regex': '^' + letters, '$options': 'i'}})
        results = [pat for pat in patients]
    else:
        return jsonify({'error': 'Invalid search type'})
    print(results)
    return JSONEncoder().encode(results)