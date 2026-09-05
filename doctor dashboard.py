"""
=========================================================================
FILE 2: MASTER DOCTOR CONTROL PANEL - AUTO ENG & RETRIEVAL
=========================================================================
"""
import psycopg2
import os

DB_CONFIG = {
    'host': 'localhost',
    'database': 'ayush_sih_db',
    'user': 'postgres',
    'password': 'root',  # <─── TYPE YOUR MASTER SETUP PASSWORD HERE!
    'port': '5432'
}

def process_automatic_doctor_assignments():
    """Loops through missing row references, updates them, and commits changes!"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Select unassigned cases using standard SQL syntax matching your terminal view
        cursor.execute("SELECT case_id, current_symptoms FROM patient_cases WHERE doctor_id IS NULL;")
        unassigned_records = cursor.fetchall()
        
        for case in unassigned_records:
            case_id, symptoms = case[0], case[1].lower()
            
            # AUTOMATIC ASSIGNMENT ENGINE: Evaluates string terms to assign Doctor ID keys
            if "joint" in symptoms or "pain" in symptoms or "fatigue" in symptoms:
                assigned_doc_id = 1  # Route to Doctor 1 (Dr. Amit Sharma - Ayurveda)
                dept = "Ayurveda"
            elif "headache" in symptoms or "migraine" in symptoms or "nausea" in symptoms:
                assigned_doc_id = 2  # Route to Doctor 2 (Dr. Kavita Rao - Homeopathy)
                dept = "Homeopathy"
            else:
                assigned_doc_id = 1  # Fallback Standard Default Doctor ID
                dept = "Ayurveda"
                
            # Execute the UPDATE query to fill the relational link column
            cursor.execute("UPDATE patient_cases SET doctor_id = %s WHERE case_id = %s;", (assigned_doc_id, case_id))
            print(f"[AUTO-ENGINE]: Case ID {case_id} analyzed. Assigned to {dept} Doctor (ID: {assigned_doc_id})")
            
        # ◄── SEALS THE UPDATE TRANSACTIONS SO AUTOMATIC ROUTING IS PERMANENT!
        conn.commit()  
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Automatic Assignment Engine Error: {e}")

def display_entire_database_summary():
    """Prints a full spreadsheet grid tracking status of all logged rows across keys"""
    print("\n==========================================================================")
    print("                MINISTRY OF AYUSH - COMPLETE CLINIC REGISTRY              ")
    print("==========================================================================")
    
    # Run our assignment engine first to make sure all records are up to date!
    process_automatic_doctor_assignments()
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Connected relational JOIN script matching every table row sitting in your terminal
        query = """
            SELECT p.patient_id, p.full_name, c.current_symptoms, d.doctor_name, c.prescription_image_path
            FROM patient_cases c
            JOIN patients p ON c.patient_id = p.patient_id
            LEFT JOIN doctors d ON c.doctor_id = d.doctor_id
            ORDER BY c.case_id DESC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if not rows:
            print("\nDatabase Locker Status: Empty. No active patient rows logged yet.")
            cursor.close()
            conn.close()
            return
            
        print(f"{'PID':<5} {'PATIENT NAME':<18} {'SYMPTOMS RECORDED':<25} {'AUTO-ASSIGNED DOCTOR':<22}")
        print("-" * 80)
        
        for record in rows:
            # Shorten symptoms string margin blocks text so column layout alignment stays neat
            short_symptoms = record[2][:22] + "..." if len(record[2]) > 22 else record[2]
            doctor_name = record[3] if record[3] else "Processing..."
            print(f"{record[0]:<5} {record[1]:<18} {short_symptoms:<25} {doctor_name:<22}")
        print("-" * 80)
        
        # REPOSITORY SELECTION OPTION: Pop open the physical screenshot file matching input ID
        view_id = input("\nEnter Patient ID to pop open their Prescription Image (or hit Enter to skip): ")
        if view_id.isdigit():
            cursor.execute("SELECT prescription_image_path FROM patient_cases WHERE patient_id = %s ORDER BY case_id DESC LIMIT 1;", (int(view_id),))
            img_result = cursor.fetchone()
            if img_result and img_result[0]:
                image_name = img_result[0]
                
            if os.path.exists(image_name):
                print(f"Success: Image found! Opening '{image_name}'...")
                os.startfile(image_name)
            else:
                print(f"Warning: Image text string '{image_name}' sits in database...")



                    
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database display error: {e}")

def main():
    while True:
        print("\n=== DOCTOR MANAGEMENT CONSOLE ===")
        print("1. View Complete Connected Database Summary & Process Auto-Assignments")
        print("2. Exit Panel")
        choice = input("Enter Choice (1-2): ")
        
        if choice == '1':
            display_entire_database_summary()
        elif choice == '2':
            break

if __name__ == "__main__":
    main()
