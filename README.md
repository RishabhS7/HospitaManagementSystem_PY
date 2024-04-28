# Hospital Management System

This project is a Hospital Management System that provides functionalities to manage patients, doctors, appointments, departments, and services. It offers APIs to interact with the system programmatically.

## Installation
To run this project locally, follow these steps:

### Install Flask:
pip install flask

### Install Flask-PyMongo:
pip install flask_pymongo

### Run the Flask application:
flask run

## API Introduction

### Add Patient
Endpoint: POST /addPatient
Description: Adds a new patient to the database.

### Get Patient by ID
Endpoint: GET /patients/{patient_id}
Description: Retrieves patient details by their unique ID.

### Update Patient
Endpoint: PUT /updatePatient/{patient_id}
Description: Updates patient information by their ID.

### Add Doctor
Endpoint: POST /addDoctor
Description: Registers a new doctor.

### Get Doctor by ID
Endpoint: GET /doctors/{doctor_id}
Description: Retrieves doctor details by their unique ID.
Update Doctor
Endpoint: PUT /updateDoctor/{doctor_id}
Description: Updates doctor information by their ID.
Add Appointment
Endpoint: POST /addAppointment
Description: Creates a new appointment for a patient with a specific doctor.

### Add Department
Endpoint: POST /addDepartment
Description: Registers a new department.

### Add Service to Department
Endpoint: POST /addServiceToDepartment
Description: Adds a new service to an existing department.

### Add Doctor to Department
Endpoint: POST /addDoctorToDepartment
Description: Assigns a doctor to an existing department.

#Search by Initial
Endpoint: GET /search?type={type}&letters={letters}
Description: Searches for departments, doctors, or patients whose names start with the provided initial letters.
