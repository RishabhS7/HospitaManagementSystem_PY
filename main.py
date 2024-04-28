from flask import Flask
from flask_pymongo import PyMongo
from flask import request, jsonify
from models import Patient,ContactInformation,MedicalHistory,Doctor,Doctor_Appointments,Patient_Appointment,Department
from flask_pymongo import ObjectId
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://rishabh7singh5:YdjNHsagAMxYX3Kb@cluster0.tiolxl3.mongodb.net/HMS"
db = PyMongo(app).db

@app.route('/')
def hello_world():  
      return 'Hello World!'

#login
# @app.route('/login', methods=["GET", "POST"])
# def login():
#     if session.get('logged_in'):
#         return redirect(url_for('logout'))
#     if request.method == 'POST':
#         username = request.form['username']
#         user_pass = request.form['password']
#         user_data = users_collection.find_one({'username': username, 'isDel': '0'})
#         if user_data:
#             password = user_data['password']
#             userlevel = user_data['level']
#             if userlevel == 'ade':
#                 permission = 'Executive'
#             elif userlevel == 'pharmacist':
#                 permission = 'Pharmacist'
#             elif userlevel == 'dse':
#                 permission = 'Diagnosist'

#             if sha256_crypt.verify(user_pass, password):
#                 session['logged_in'] = True
#                 session['userlevel'] = userlevel
#                 session['username'] = username
#                 session['permission'] = permission
#                 flash('Logged In Successfully!!!', 'success')
#                 return redirect(url_for('dashboard'))
#             else:
#                 flash('Invalid Login', 'danger')
#                 return redirect(url_for('login'))
#         else:
#             flash('User Not Found', 'danger')
#             return redirect(url_for('login'))

#     return render_template('login.html')
# Custom JSON encoder to handle ObjectId serialization
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o) 


@app.route('/addPatient',methods=['POST'])
def add_patient():
    data = request.get_json()
    if not data.get('name') or not data.get('age') or not data.get('gender'):
        return jsonify({'error': 'Missing username, email, or password'}), 400

    existing_patient = db.patients.find_one({'contact_information.email': data.get('email')})
    if existing_patient:
        return jsonify({'error': 'Email already registered'}), 400
    
    medical_history = MedicalHistory(previous_diagnoses=[],allergies=[],medications=[]).to_dict()
    contact_info = ContactInformation(phone=data['contact_information']['phone'], email=data['contact_information']['email'], address=data['contact_information']['address'],).to_dict()
    patient = Patient(name=data['name'], age=data['age'], gender=data['gender'], contact_information=contact_info, medical_history=medical_history, appointment_records=[])
    db.patients.insert_one(vars(patient))
    return jsonify({'message': 'User registered successfully'}), 201

# Define the route to get a patient by ID
@app.route('/patients/<string:patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    # patient_id = request.args.get('patient_id')  
    print("here")
    patient = db.patients.find_one({'_id': ObjectId(patient_id)})
    return JSONEncoder().encode(patient)

# Define the route to update a patient
@app.route('/updatePatient/<patient_id>', methods=['PUT'])
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

# route to add a new doctor
@app.route('/addDoctor',methods=['POST'])
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
@app.route('/doctors/<doctor_id>', methods=['GET'])
def get_doctor_by_id(doctor_id):
    doctor = db.doctors.find_one_or_404({'_id': ObjectId(doctor_id)})
    # Assuming you have implemented a method to convert doctor object to JSON
    return JSONEncoder().encode(doctor)

# Define the route to update a patient
@app.route('/updateDoctor/<doctor_id>', methods=['PUT'])
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
@app.route('/addAppointment', methods=['POST'])
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

# route to add a new doctor
@app.route('/addDepartment',methods=['POST'])
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

@app.route('/addServiceToDepartment', methods=['POST'])
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

@app.route('/addDoctorToDepartment', methods=['POST'])
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

   

@app.route('/search', methods=['GET'])
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

if __name__ == "__main__":
    app.run(debug=True,port=5000)

    # YdjNHsagAMxYX3Kb
    # mongodb+srv://rishabh7singh5:YdjNHsagAMxYX3Kb@cluster0.tiolxl3.mongodb.net/