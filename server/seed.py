"""
Database seeding script for TibaCare Hospital Management System.
This script populates the database with initial data.

Usage:
    python seed.py
"""

from models import Patient, Appointment, Doctor, Department, db
from datetime import datetime
from faker import Faker
import random


def seed_database(app, bcrypt):
    """
    Seed the database with initial data.
    
    Args:
        app: Flask application instance
        bcrypt: Bcrypt instance for password hashing
    """
    faker = Faker()

    with app.app_context():
        print("Clearing db ...")
        db.drop_all()  # Optional: Clear all tables (ensure you want to do this)
        db.create_all()  # Recreate tables after dropping them
        Doctor.query.delete()
        Patient.query.delete()
        Department.query.delete()
        Appointment.query.delete()

        print("Seeding Department data...")

        departments_data = [
            { 'name': 'Emergency', 'image': 'emergency.jpg' },
            { 'name': 'Cardiology', 'image': 'cardiology.jpg' },
            { 'name': 'Neurology', 'image': 'neurology.jpg' },
            { 'name': 'Pediatrics', 'image': 'pediatrics.jpg' },
            { 'name': 'Orthopedics', 'image': 'orthopedics.jpg' },
            { 'name': 'Gynecology', 'image': 'gynecology.jpg' },
            { 'name': 'General Surgery', 'image': 'general_surgery.jpg' },
            { 'name': 'Optometry', 'image': 'optometry.jpg' },
            { 'name': 'Radiology', 'image': 'radiology.jpg' },
            { 'name': 'ENT', 'image': 'ent.jpg' },
            { 'name': 'Oncology', 'image': 'oncology.jpg' },
            { 'name': 'Urology', 'image': 'urology.jpg' },
            { 'name': 'Dentistry', 'image': 'dentistry.jpg' },
            { 'name': 'Dermatology', 'image': 'dermatology.jpg' },
            { 'name': 'Nephrology', 'image': 'nephrology.jpg' },
            { 'name': 'Psychiatry', 'image': 'psychiatry.jpg' },
        ]

        # Seed data into the database
        for department_data in departments_data:
            department = Department(
                name=department_data['name'],
                description=faker.text(),
                image=department_data['image']
            )
            db.session.add(department)

        db.session.commit()

        print("Seeding Doctor data...")

        doctors_data = [
            # Emergency Department (Department 1)
            { 'name': 'Dr. Michael Ndungu', 'specialty': 'Emergency Physician', 'image': 'Dr45.jpg', 'department_id': 1 },
            { 'name': 'Dr. Sarah Onyango', 'specialty': 'Trauma Surgeon', 'image': 'Dr46.jpg', 'department_id': 1 },
            { 'name': 'Dr. James Wambui', 'specialty': 'Emergency Physician', 'image': 'Dr47.jpg', 'department_id': 1 },
            { 'name': 'Dr. Linda Njoroge', 'specialty': 'Critical Care Specialist', 'image': 'Dr48.jpg', 'department_id': 1 },
            { 'name': 'Dr. Peter Mwangi', 'specialty': 'Emergency Physician', 'image': 'Dr49.jpg', 'department_id': 1 },
            { 'name': 'Dr. Nancy Omondi', 'specialty': 'Emergency Physician', 'image': 'Dr50.jpg', 'department_id': 1 },
            
            # Cardiology (Department 2)
            { 'name': 'Dr. John Kamau', 'specialty': 'Cardiologist', 'image': 'Dr1.jpg', 'department_id': 2 },
            { 'name': 'Dr. Jane Mwangi', 'specialty': 'Cardiologist', 'image': 'Dr2.jpg', 'department_id': 2 },
            { 'name': 'Dr. Allan Wekesa', 'specialty': 'Cardiologist', 'image': 'Dr3.jpg', 'department_id': 2 },
            { 'name': 'Dr. Susan Otieno', 'specialty': 'Cardiologist', 'image': 'Dr4.jpg', 'department_id': 2 },

            # Neurology (Department 3)
            { 'name': 'Dr. Peter Odhiambo', 'specialty': 'Neurologist', 'image': 'Dr5.jpg', 'department_id': 3 },
            { 'name': 'Dr. Ann Wanjiru', 'specialty': 'Neurologist', 'image': 'Dr6.jpg', 'department_id': 3 },
            { 'name': 'Dr. David Maina', 'specialty': 'Neurologist', 'image': 'Dr7.jpg', 'department_id': 3 },
            { 'name': 'Dr. Angela Mwangi', 'specialty': 'Neurologist', 'image': 'Dr8.jpg', 'department_id': 3 },

            # Pediatrics (Department 4)
            { 'name': 'Dr. Sarah Njeri', 'specialty': 'Pediatrician', 'image': 'Dr21.jpg', 'department_id': 4 },
            { 'name': 'Dr. Richard Kamau', 'specialty': 'Pediatrician', 'image': 'Dr22.jpg', 'department_id': 4 },
            { 'name': 'Dr. Fiona Wambui', 'specialty': 'Pediatrician', 'image': 'Dr23.jpg', 'department_id': 4 },
            { 'name': 'Dr. Kevin Otieno', 'specialty': 'Pediatrician', 'image': 'Dr24.jpg', 'department_id': 4 },

            # Orthopedics (Department 5)
            { 'name': 'Dr. Samuel Otieno', 'specialty': 'Orthopedic Surgeon', 'image': 'Dr9.jpg', 'department_id': 5 },
            { 'name': 'Dr. Lucy Wanjiru', 'specialty': 'Orthopedic Surgeon', 'image': 'Dr10.jpg', 'department_id': 5 },
            { 'name': 'Dr. Anthony Mburu', 'specialty': 'Orthopedic Surgeon', 'image': 'Dr11.jpg', 'department_id': 5 },

            # Gynecology (Department 6)
            { 'name': 'Dr. Jack Mwangi', 'specialty': 'Gynecologist', 'image': 'Dr38.jpg', 'department_id': 6 },
            { 'name': 'Dr. Carol Njeri', 'specialty': 'Gynecologist', 'image': 'Dr39.jpg', 'department_id': 6 },

            # General Surgery (Department 7)
            { 'name': 'Dr. Michael Wekesa', 'specialty': 'General Surgeon', 'image': 'Dr25.jpg', 'department_id': 7 },
            { 'name': 'Dr. Evelyn Wanjiru', 'specialty': 'General Surgeon', 'image': 'Dr26.jpg', 'department_id': 7 },
            { 'name': 'Dr. Charles Mburu', 'specialty': 'General Surgeon', 'image': 'Dr27.jpg', 'department_id': 7 },
        ]

        # Seed data into the database
        for doctor_data in doctors_data:
            doctor = Doctor(
                title="Dr.",
                doctorId=faker.random_number(digits=5, fix_len=True),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                bio=faker.text(),
                education=faker.text(),
                certifications=faker.text(),
                image=doctor_data['image'],
                specialty=doctor_data['specialty'],
                department_id=doctor_data['department_id'],
                password=bcrypt.generate_password_hash('1234Abcd').decode('utf-8')
            )
            db.session.add(doctor)

        db.session.commit()

        print("Seeding Patient data...")
        
        patients = []
        genders = ['Male', 'Female', 'Other']
        for _ in range(100):
            patient = Patient(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                age=faker.random_int(18, 99),
                gender=random.choice(genders),
                email=faker.unique.email(),
                phone_number=faker.phone_number(),
                password=bcrypt.generate_password_hash('1234Abcd').decode('utf-8')
            )
            patients.append(patient)
        db.session.add_all(patients)
        db.session.commit()

        print("Seeding Appointment data...")
        appointments = []
        for _ in range(100):
            time_str = faker.time()  
            time_obj = datetime.strptime(time_str, '%H:%M:%S').time()

            appointment = Appointment(
                date=faker.date_this_year(),
                time=time_obj,  
                medical_records=faker.text(),
                patient_id=random.randint(1, 100),
                doctor_id=random.randint(1, 50) 
            )
            appointments.append(appointment)

        db.session.add_all(appointments)
        db.session.commit()

        print("Database seeded successfully!")


if __name__ == "__main__":
    # Import here to avoid circular dependency at module load time
    from app import app, bcrypt
    seed_database(app, bcrypt)
