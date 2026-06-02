from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin as sm
import datetime
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Patient(db.Model, sm):
    __tablename__ = 'patients'
    
    serialize_rules = ("-appointments.patient", "-appointments.doctor", "-doctors")

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    appointments = db.relationship("Appointment", back_populates="patient")
    doctors = association_proxy("appointments", "doctor", creator=lambda doctor_obj: Appointment(doctor=doctor_obj))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "gender": self.gender,
            "email": self.email,
            "phone_number": self.phone_number,
            "medical_records": [appointment.medical_records for appointment in self.appointments],
            "appointments": [appointment.to_dict() for appointment in self.appointments]
        }

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name} {self.email}>"

class Appointment(db.Model, sm):
    __tablename__ = 'appointments'

    serialize_rules = ("-patient.appointments", "-doctor.appointments")

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    medical_records = db.Column(db.String, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))

    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")

    def to_dict(self):
        return {
            "id": self.id,
            "time": str(self.time),
            "date": self.date.strftime('%Y-%m-%d %H:%M:%S'),
            "medical_records": self.medical_records,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
        }

    def __repr__(self):
        return f"<Appointment {self.patient_id} {self.doctor_id}>"

class Department(db.Model, sm):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)

    doctors = db.relationship("Doctor", back_populates="department")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "doctors": [doctor.to_dict() for doctor in self.doctors]  # New field for doctor list in department dictionary. This is an association proxy that automatically fetches and manages related doctor objects.  # New field for doctor list in department dictionary. This is an association proxy that automatically fetches and manages related doctor objects.  # New field for doctor list in department dictionary. This is an association proxy that automatically fetches and manages related doctor objects.  # New
        }

    def __repr__(self):
        return f"<Department {self.name}>"

class Doctor(db.Model, sm):
    __tablename__ = "doctors"

    serialize_rules = ("-appointments.doctor", "-appointments.patient", "-patients")

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    doctorId = db.Column(db.String)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String, unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    bio = db.Column(db.Text)
    education = db.Column(db.String)
    certifications = db.Column(db.String)
    specialty = db.Column(db.String(50))
    image = db.Column(db.String(200))
    password = db.Column(db.String, nullable=False)
   
    appointments = db.relationship("Appointment", back_populates="doctor")
    department = db.relationship("Department", back_populates="doctors")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "doctorId": self.doctorId,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "bio": self.bio,
            "education": self.education,
            "certifications": self.certifications,
            "specialty": self.specialty,
            "image": self.image,
            "department_id": self.department_id,
        }

    def to_card_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "specialty": self.specialty,
            "image": self.image,
        }

    def to_profile_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "doctorId": self.doctorId,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "bio": self.bio,
            "education": self.education,
            "certifications": self.certifications,
            "specialty": self.specialty,
            "image": self.image,
            "department_id": self.department_id,
        }

    def __repr__(self):
        return f"<Doctor {self.first_name} {self.last_name}>"
