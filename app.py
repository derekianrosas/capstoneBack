from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASURE_URI"] = ""

db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)

class VehicleRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(), nullable=False)
    model = db.Column(db.String(), nullable=False)
    miles = db.Column(db.String(), nullable=False)
    year = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    
    def __init__(self, manufacturer, model, miles, year, description):
        self.manufacturer = manufacturer
        self.model = model
        self.miles = miles
        self.year = year
        self.description = description
    
class VehicleRecordSchema(ma.Schema):
    class Meta:
        fields = ("id", "manufacturer", "model", "miles", "year", "description")

vehicle_record_schema = VehicleRecordSchema()
multiple_record_schema = VehicleRecordSchema(many=True)

if __name__ == "__main__":
    app.run(debug=True)