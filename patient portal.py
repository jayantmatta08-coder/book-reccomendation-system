"""
======================================================
AYUSH PATIENT CASE SHEET & MEDICAL HISTORY SYSTEM (SIH)
======================================================
"""

import psycopg2  # Changed library from mysql.connector
import os
from datetime import datetime

# Database Configuration (Using default PostgreSQL parameters)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'root', # Change to the password you just set in installation
    'database': 'ayush_sih_db',
    'port': '5432'
}

conn = None

# ==================== DATABASE CONFIGURATION & TABLES ====================

def initialize_database():
    """Connect to Postgres and create required tables if they do not exist"""
    global conn
    try:
        # Connect to default postgres cluster first to create your hackathon database safely
        temp_conn = psycopg2.connect(host=DB_CONFIG['host'], user=DB_CONFIG['user'], password=DB_CONFIG['password'], port=DB_CONFIG['port'], database='postgres')
        temp_conn.autocommit = True
        temp_cursor = temp_conn.cursor()
        
        # Check if database already exists
        temp_cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'ayush_sih_db';")
        exists = temp_cursor.fetchone()
        if not exists:
            temp_cursor.execute("CREATE DATABASE ayush_sih_db;")
            print("Database 'ayush_sih_db' created successfully!")
            
        temp_cursor.close()
        temp_conn.close()

        # Connect to our brand new AYUSH database
        conn = psycopg2.connect(**DB_CONFIG)
        print("Connected to PostgreSQL successfully!")
        
        # Call table creation routine
        create_tables()
        return True
    except Exception as err:
        print(f"Connection Initialization Error: {err}")
        return False

def create_tables():
    """Create all required tables for doctors, patients, history, and cases"""
    cursor = conn.cursor()
    
    # 1. Create Doctors Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id SERIAL PRIMARY KEY,
            doctor_name VARCHAR(100),
            ayush_department VARCHAR(50)
        )
    """)
    
    # 2. Create Core Patients Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id SERIAL PRIMARY KEY,
            full_name VARCHAR(100),
            age INT,
            gender VARCHAR(20)
        )
    """)
    
    # 3. Create Permanent Medical History Table (Your primary workflow addition!)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_history (
            history_id SERIAL PRIMARY KEY,
            patient_id INT,
            past_illnesses TEXT,
            known_allergies TEXT
        )
    """)
    
    # 4. Create Patient Cases Table (Where your prescription picture logic is!)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_cases (
            case_id SERIAL PRIMARY KEY,
            patient_id INT,
            doctor_id INT,
            current_symptoms TEXT,
            diagnosis_notes TEXT,
            
            -- IMAGE COLUMN OPTION: This saves the file link as plain text string data
            prescription_image_path VARCHAR(500),
            created_at DATE
        )
    """)
    
    conn.commit()
    cursor.close()
    print("All clinical database structures generated successfully!")


# ==================== MAIN CORE FEATURES ====================

def register_patient_profile():
    """Add a new patient and instantly record their history background text"""
    print("\n=== REGISTER NEW PATIENT PROFILE ===")
    name = input("Patient Full Name: ")
    age = int(input("Age: "))
    gender = input("Gender (Male/Female/Other): ")
    
    # Gathering historical assessment logs
    past_illnesses = input("Chronic Past Illnesses (e.g. Diabetes, BP, None): ")
    allergies = input("Known Substance/Drug Allergies (or None): ")
    
    try:
        cursor = conn.cursor()
        
        # Query A: Log Core demographics (Uses standard %s formatting)
        query_patient = "INSERT INTO patients (full_name, age, gender) VALUES (%s, %s, %s) RETURNING patient_id;"
        cursor.execute(query_patient, (name, age, gender))
        new_patient_id = cursor.fetchone()[0]
        
        # Query B: Log historical entries mapped directly to that patient ID
        query_history = "INSERT INTO medical_history (patient_id, past_illnesses, known_allergies) VALUES (%s, %s, %s);"
        cursor.execute(query_history, (new_patient_id, past_illnesses, allergies))
        
        conn.commit()
        print(f"\nSuccess: Profile created! Assigned Patient ID is: {new_patient_id}")
        cursor.close()
    except Exception as e:
        print(f"Error executing entry registration: {e}")


def upload_new_consultation_case():
    """Log current symptoms, diagnosis and include a local image file path configuration"""
    print("\n=== RECORD NEW LOGS & PRESCRIPTION PICTURE ===")
    patient_id = int(input("Enter Existing Patient ID: "))
    doctor_id = int(input("Enter Your Doctor ID: "))
    symptoms = input("Current Symptoms: ")
    diagnosis = input("Clinical Diagnosis Remarks: ")
    
    # IMAGE SUBMISSION HANDLER:
    print("\n[IMAGE INSTRUCTIONS]: Move the prescription photo into your project folder.")
    image_filename = input("Type the exact name of the file (e.g. prescription1.jpg): ")
    
    # We define a standard project folder path string where images are safely organized
    target_folder = "project_images/"
    full_image_link_path = target_folder + image_filename

    try:
        cursor = conn.cursor()
        today_date = datetime.now().date()
        
        # Execute query passing file location tracking string directly into database text parameters
        query_case = """
            INSERT INTO patient_cases (patient_id, doctor_id, current_symptoms, diagnosis_notes, prescription_image_path, created_at)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query_case, (patient_id, doctor_id, symptoms, diagnosis, full_image_link_path, today_date))
        conn.commit()
        
        print("\nSuccess: Consultation logs saved!")
        print(f"Prescription path recorded inside database as text: '{full_image_link_path}'")
        cursor.close()
    except Exception as e:
        print(f"Error updating logs table: {e}")


def view_complete_medical_history():
    """Fetch complete history log timeline view for a doctor using a clean SQL JOIN"""
    print("\n=== RETRIEVE COMPREHENSIVE MEDICAL HISTORY ===")
    search_id = int(input("Enter Patient ID to look up: "))
    
    cursor = conn.cursor()
    
    # Clean standard Class 12 SQL JOIN query pulling background history and timeline records
    query = """
        SELECT p.full_name, p.age, h.past_illnesses, h.known_allergies, 
               c.created_at, c.current_symptoms, c.diagnosis_notes, c.prescription_image_path
        FROM patients p
        LEFT JOIN medical_history h ON p.patient_id = h.patient_id
        LEFT JOIN patient_cases c ON p.patient_id = c.patient_id
        WHERE p.patient_id = %s
        ORDER BY c.created_at DESC;
    """
    cursor.execute(query, (search_id,))
    records = cursor.fetchall()
    
    if not records:
        print("No matches or historical timelines found for that ID.")
        cursor.close()
        return

    # Print static demographic information out of first index tuple row position
    print("\n" + "="*60)
    print(f"PATIENT NAME : {records[0][0]}  |  AGE: {records[0][1]}")
    print(f"PAST CHRONIC ILLNESSES: {records[0][2]}")
    print(f"KNOWN RECORDED ALLERGIES: {records[0][3]}")
    print("="*60)
    print(f"{'VISIT DATE':<12} {'SYMPTOMS RECORDED':<25} {'DIAGNOSIS':<20}")
    print("-"*60)
    
    # Loop printing each individual visit tracking path log down the command line
    for row in records:
        if row[4]: # Check if any consultation case entry exists for that date index loop row
            print(f"{str(row[4]):<12} {row[5]:<25} {row[6]:<20}")
            print(f"└─► Link to Prescription Picture: {row[7]}")
            print("-"*60)
            
    cursor.close()


# ==================== MAIN INTERACTIVE CONTROLLER ====================

def main_menu():
    """Clean Class 12 selection loop interface controller"""
    while True:
        print("\n" + "=" * 50)
        print("MINISTRY OF AYUSH - PATIENT PORTAL SYSTEM")
        print("=" * 50)
        print("1. Register New Patient Profile & Past History")
        print("2. Record New Consultation Visit + Image Upload")
        print("3. View Complete Patient Record History (For Doctor)")
        print("4. Exit Application")
        
        choice = input("\nEnter Choice (1-4): ")
        
        if choice == '1':
            register_patient_profile()
        elif choice == '2':
            upload_new_consultation_case()
        elif choice == '3':
            view_complete_medical_history()
        elif choice == '4':
            print("\nShutting down portal. Good luck with the SIH presentation!")
            break
        else:
            print("Invalid input selection option. Try again.")

if __name__ == "__main__":
    if initialize_database():
        main_menu()
        if conn:
            conn.close()
