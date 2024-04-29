from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://rishabh7singh5:YdjNHsagAMxYX3Kb@cluster0.tiolxl3.mongodb.net/HMS"
db = PyMongo(app).db