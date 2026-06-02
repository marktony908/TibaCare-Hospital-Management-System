from flask import Flask, request, session, make_response,jsonify, send_from_directory
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource
from flask_cors import CORS
from sqlalchemy.orm import joinedload

from models import db, Doctor, Department, Patient, Appointment
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration with environment variables
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:4000')

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Only set SECURE cookie in production
app.config['SESSION_COOKIE_SECURE'] = ENVIRONMENT == 'production'
app.json.compact = False

migrate = Migrate(app, db)
api = Api(app)
bcrypt = Bcrypt(app)

# Parse CORS origins from environment variable
cors_origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(',')]
CORS(app, supports_credentials=True, resources={r"/*": {"origins": cors_origins}})

db.init_app(app)



class Images(Resource):
    def get(self):
        # Get the model type and filename from query parameters
        model_type = request.args.get('model').lower()  # Convert to lowercase
        filename = request.args.get('filename')

        if not filename:
            return {"message": "Filename is required"}, 400

        # Determine the model and fetch the image
        if model_type == 'doctor':
            doctor = Doctor.query.filter_by(image=filename).first()  # Adjust based on your field
            if doctor:
                return send_from_directory(UPLOAD_FOLDER, filename)
            else:
                return {"message": "Doctor image not found"}, 404

        elif model_type == 'department':
            department = Department.query.filter_by(image=filename).first()  # Adjust based on your field
            if department:
                return send_from_directory(UPLOAD_FOLDER, filename)
            else:
                return {"message": "Department image not found"}, 404

        return {"message": "Invalid model type"}, 400

    
class DoctorsByDepartment(Resource):
    def get(self, id):
        department = Department.query.filter_by(id=id).first()
        if not department:
            return {"error": "Department not found"}, 404
        doctors_dict = [doctor.to_dict() for doctor in department.doctors]
        return make_response(doctors_dict, 200)


class DoctorProfile(Resource):
    def get(self, id):
        doctor = Doctor.query.filter_by(id=id).first()
        return make_response(doctor.to_dict(), 200)

class DoctorSignup(Resource):
    def post(self):
        data = request.form
        image = request.files.get('image')
        
        # Store only filename, not full path
        filename = None
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            
        new_doctor = Doctor(
            title=data.get('title'),
            doctorId=data.get('doctorId'),
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            email=data.get('email'),
            bio=data.get('bio'),
            education=data.get('education'),
            certifications=data.get('certifications'),
            specialty=data.get('specialty'),
            image=filename,  # Store only filename
            department_id=data.get('department'),
            password=bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
        )

        try:
            db.session.add(new_doctor)
            db.session.commit()
            return new_doctor.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

class DoctorLogin(Resource):
    def post(self):
        data = request.get_json() 
        doctor = Doctor.query.filter_by(email=data['email']).first()

        if doctor and bcrypt.check_password_hash(doctor.password, data['password']):
            session['user_id'] = doctor.id
            session['user_role'] = 'doctor'
            return {
                "message": "Login successful",
                "data": doctor.to_dict(),
                "status": 200
            }
        else:
            return {"error": "Invalid credentials"}, 401
        
class PatientSignup(Resource):
    def post(self):
        data = request.get_json()

        new_patient = Patient(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            age=int(data.get('age')),
            phone_number=data.get('phone_number'),
            gender=data.get('gender'),
            password=bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
        )

        try:
            db.session.add(new_patient)
            db.session.commit()
            return new_patient.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

class PatientLogin(Resource):
    def post(self):
        data = request.get_json() 
        
        patient = Patient.query.filter_by(email=data['email']).first()

        if patient and bcrypt.check_password_hash(patient.password, data['password']):
            session['user_id'] = patient.id
            session['user_role'] = 'patient'
            
            return {
                    "message": "Login successful",
                    "data": patient.to_dict(),
                    "status": 200
                }, 200
        else:
            return {"error": "Invalid email or password"}, 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

# Check Session Resource
class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        user_role = session.get('user_role')

        if user_id and user_role:
            if user_role == 'doctor':
                user = Doctor.query.get(user_id)
            elif user_role == 'patient':
                user = Patient.query.get(user_id) 
            if user:
                return {
                    "user": user.to_dict(),
                    "role": user_role 
                }, 200
            else:
                return {"error": "User not found"}, 404
        return {"error": "Unauthorized"}, 401
    
class DoctorById(Resource):
    def get(self, id):
        doctor = Doctor.query.filter_by(id=id).first()
        return make_response(doctor.to_dict(),200)

class DepartmentList(Resource):
    def get(self):
        departments_dict =[department.to_dict() for department in Department.query.all()]
        return make_response(departments_dict, 200)
    
class PatientById(Resource):
    def get(self, id):
        patient = Patient.query.filter_by(id=id).first()
        return make_response(patient.to_dict(),200)
        
class AppointmentResource(Resource):
    def get(self, appointment_id=None):
        # If appointment_id is provided, fetch a single appointment
        if appointment_id:
            appointment = Appointment.query.options(
                joinedload(Appointment.patient), joinedload(Appointment.doctor)
            ).filter_by(id=appointment_id).first()

            if not appointment:
                return {"error": "Appointment not found"}, 404

            return jsonify(appointment.to_dict())

        # Otherwise, return all appointments
        appointments = Appointment.query.options(
            joinedload(Appointment.patient), joinedload(Appointment.doctor)
        ).all()

        return jsonify([appointment.to_dict() for appointment in appointments])


# Register API Resources
api.add_resource(DoctorSignup, '/api/doctorsignup', endpoint='doctorsignup')
api.add_resource(DoctorLogin, '/api/doctorlogin', endpoint='doctorlogin')
api.add_resource(Logout, '/api/logout', endpoint=None)
api.add_resource(CheckSession, '/api/check_session', endpoint='check_session')
api.add_resource(PatientSignup, '/api/patientsignup', endpoint='patientsignup')
api.add_resource(PatientLogin, '/api/patientlogin', endpoint='patientlogin')
api.add_resource(DoctorById, '/api/doctor/<int:id>')
api.add_resource(PatientById, '/api/patient/<int:id>')
api.add_resource(AppointmentResource, '/api/appointments', '/api/appointments/<int:appointment_id>')
api.add_resource(DepartmentList, '/api/departments', endpoint='departments')
api.add_resource(DoctorsByDepartment, '/api/departments/<int:id>')
api.add_resource(DoctorProfile, '/api/doctors/<int:id>')
api.add_resource(Images, '/api/images')

if __name__ == "__main__":
    app.run(port=5555)
