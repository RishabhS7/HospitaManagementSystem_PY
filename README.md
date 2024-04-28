Hospital Management System
This project is a Hospital Management System that provides functionalities to manage patients, doctors, appointments, departments, and services. It offers APIs to interact with the system programmatically.

Installation
To run this project locally, follow these steps:

Install Flask:
pip install flask

Install Flask-PyMongo:
pip install flask_pymongo

Run the Flask application:
flask run

API Introduction
Add Patient
Endpoint: POST /addPatient
Description: Adds a new patient to the database.
Request Body:

{
"name": "string",
"age": "string",
"gender": "string",
"contact_information": {
"phone": "string",
"email": "string",
"address": "string"
}
}
Get Patient by ID
Endpoint: GET /patients/{patient_id}
Description: Retrieves patient details by their unique ID.
Update Patient
Endpoint: PUT /updatePatient/{patient_id}
Description: Updates patient information by their ID.
Add Doctor
Endpoint: POST /addDoctor
Description: Registers a new doctor.
Request Body:
{
"name": "string",
"specialization": "string",
"contact_information": {
"phone": "string",
"email": "string",
"address": "string"
},
"start_time": "string",
"total_shift_time": "string",
"break_start_time": "string"
}
Get Doctor by ID
Endpoint: GET /doctors/{doctor_id}
Description: Retrieves doctor details by their unique ID.
Update Doctor
Endpoint: PUT /updateDoctor/{doctor_id}
Description: Updates doctor information by their ID.
Add Appointment
Endpoint: POST /addAppointment
Description: Creates a new appointment for a patient with a specific doctor.
Request Body:

{
"doctor_id": "string",
"patient_id": "string",
"date": "string",
"time": "string",
"duration_in_minutes": "string",
"department": "string"
}
Add Department
Endpoint: POST /addDepartment
Description: Registers a new department.
Request Body:

{
"name": "string",
"services": ["string"],
"doctors_assigned": ["string"]
}
Add Service to Department
Endpoint: POST /addServiceToDepartment
Description: Adds a new service to an existing department.
Request Body:

{
"department_name": "string",
"service": "string"
}
Add Doctor to Department
Endpoint: POST /addDoctorToDepartment
Description: Assigns a doctor to an existing department.
Request Body:
{
"department_name": "string",
"doctor_name": "string"
}
Search by Initial
Endpoint: GET /search?type={type}&letters={letters}
Description: Searches for departments, doctors, or patients whose names start with the provided initial letters.
