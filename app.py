from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://qdhxhgochdraxa:44fe4bee2c1ae599a683c3323e8353f97908904710c765007a1f50fbe0aa9363@ec2-35-172-85-250.compute-1.amazonaws.com:5432/d2da13lph59jgg"

db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)
bcrypt = Bcrypt(app)

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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id","username","password")

user_schema = UserSchema()
users_schema = UserSchema(many=True)



@app.route("/vehicle-record/add-vehicle", methods=["POST"])
def add_vehicle():

    manufacturer = request.form.get("manufacturer")
    model = request.form.get("model")
    miles = request.form.get("miles")
    year = request.form.get("year")
    description = request.form.get("description")
    
    record = VehicleRecord(manufacturer, model, miles, year, description)
    db.session.add(record)
    db.session.commit()
    
    return jsonify("Vehicle added successfully")

@app.route("/vehicle-record/get", methods=["GET"])
def get_all_vehicles():
    all_vehicles = db.session.query(VehicleRecord).all()
    return jsonify(multiple_record_schema.dump(all_vehicles))

@app.route("/user/create", methods=["POST"])
def create_user():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")
    
    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    username_check = db.session.query(User.username).filter(User.username == username).first()

    if username_check is not None:
        return jsonify("Username Unavailable")

    hashed_password = bcrypt.generate_password_hash(password).decode("utf8")    
    
    record = User(username, hashed_password)
    db.session.add(record)
    db.session.commit()

    return jsonify("User Created Successfully")

@app.route("/user/get", methods=["GET"])
def get_all_users():
    all_users = db.session.query(User).filter(User.id == id).first()
    return jsonify(users_schema.dump(all_users))

@app.route("/user/get/<id>", methods=["GET"])
def get_single_user():
    user = db.session.query(User).filter(User.id == id).first()
    return jsonify(user_schema.dump(user))

@app.route("/user/verification", methods=["POST"])
def verify_user():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")
    
    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    stored_password = db.session.query(User.password).filter(User.username == username).first()

    if stored_password is None:
        return jsonify("User NOT Verified")
    
    valid_password_check = bcrypt.check_password_hash(stored_password[0], password)

    if valid_password_check == False:
        return jsonify("User NOT Verified")

    return jsonify("User Verified")



if __name__ == "__main__":
    app.run(debug=True)
    