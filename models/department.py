
# Define the schema for the patient collection
class Department:
    def __init__(self, name, services=[], doctors_assigned=[]):
        self.name = name
        self.services = services
        self.doctors_assigned = doctors_assigned