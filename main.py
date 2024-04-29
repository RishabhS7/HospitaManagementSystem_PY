from configs.app import app
from routes.patientRoutes import patient_blueprint
from routes.doctorRoutes import doctor_blueprint
from routes.departmentRoutes import department_blueprint

app.register_blueprint(patient_blueprint)
app.register_blueprint(doctor_blueprint)
app.register_blueprint(department_blueprint)

@app.route('/')
def hello_world():  
      return 'Hello World!'

if __name__ == "__main__":
    app.run(debug=True,port=5000)