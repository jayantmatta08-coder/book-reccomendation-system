from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI()

# 🌐 INTEROPERABILITY MIDDLEWARE: Removes security barrier connection blocks during integration testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permits your team's frontend project address to hit this service layer smoothly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔗 CLOUD BACKEND CREDENTIAL LINKAGE: Provide your authentic network parameters here
# Found inside: Supabase Dashboard Workspace -> Project Settings (Gear Icon) -> API
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "your-actual-anon-key-string-goes-here"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==================== CLOUD MIGRATED FUNCTION ENDPOINTS ====================

@app.post("/api/register-patient")
def register_patient_profile(
    user_id: str = Form(...),       # Captures unique security string tokens pushed from user login sequences
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    abha_number: str = Form(None)   # Optional Government Health Registry number input parameters
):
    """Upgraded implementation of your patient metadata capture workflows targeting cloud spaces"""
    try:
        patient_data = {
            "user_id": user_id,
            "full_name": name,
            "age": age,
            "gender": gender,
            "abha_number": abha_number
        }
        # Object routing methods cleanly target hosted databases without string injection exposures
        response = supabase.table("patients").insert(patient_data).execute()
        return {"status": "Success", "patient": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/save-medical-history")
def save_medical_history(
    patient_id: int = Form(...),
    past_illnesses: str = Form(...),
    known_allergies: str = Form(...)
):
    """Persists historical background parameters (Allergies, chronic markers) from your original logic"""
    try:
        history_payload = {
            "patient_id": patient_id,
            "past_illnesses": past_illnesses,
            "known_allergies": known_allergies
        }
        response = supabase.table("medical_history").insert(history_payload).execute()
        return {"status": "Success", "history": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload-consultation")
async def upload_new_consultation_case(
    patient_id: int = Form(...),
    symptoms: str = Form(...),
    diagnosis: str = Form(...),
    file: UploadFile = File(...)     # Natively handles file streams uploaded over active connection ports
):
    """Streams prescription images directly to cloud file storage buckets and processes cases with AI OCR data"""
    try:
        # 1. READ PHYSICAL FILE INPUT AS RAW BYTES STREAM & PIPELINE DIRECTLY INTO THE CLOUD BUCKET
        file_bytes = await file.read()
        cloud_file_path = f"prescriptions/{patient_id}_{file.filename}"
        
        supabase.storage.from_("prescriptions").upload(
            path=cloud_file_path,
            file=file_bytes,
            file_options={"content-type": file.content_type}
        )
        
        # Pull down the clean public web URL destination tracking string address
        public_url = supabase.storage.from_("prescriptions").get_public_url(cloud_file_path)
        
        # 2. RUNS YOUR AUTOMATIC ASSIGNMENT ENGINE LOGIC (Ported directly from your original File 2 code blocks)
        symptoms_lower = symptoms.lower()
        if "joint" in symptoms_lower or "pain" in symptoms_lower or "fatigue" in symptoms_lower:
            assigned_doc_id = 1  # Route parameters map directly to Dr. Amit Sharma (Ayurveda)
        elif "headache" in symptoms_lower or "migraine" in symptoms_lower or "nausea" in symptoms_lower:
            assigned_doc_id = 2  # Route parameters map directly to Dr. Kavita Rao (Homeopathy)
        else:
            assigned_doc_id = 1  # Standard System Fallback Master Key Assignment
            
        # 3. AI ASSISTANT CLINICAL OCR PROCESSING LAYER MOCK CONTAINER
        mock_ai_ocr_text = "AI EXTRACTED MEDICINE DATA: Ashwagandha - 500mg, Dashmularishta - 15ml post meals."
        
        # 4. DISPATCH AN INTEGRATED DATA DICTIONARY PAYLOAD DOWN TO CLOUD HISTORICAL SYSTEM REGISTRIES
        case_payload = {
            "patient_id": patient_id,
            "doctor_id": assigned_doc_id,
            "current_symptoms": symptoms,
            "diagnosis_notes": diagnosis,
            "prescription_image_url": public_url,
            "ai_extracted_text": mock_ai_ocr_text
        }
        supabase.table("patient_cases").insert(case_payload).execute()
        
        return {
            "status": "Success", 
            "assigned_doctor_id": assigned_doc_id, 
            "image_url": public_url,
            "ai_extracted_text": mock_ai_ocr_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/comprehensive-history/{patient_id}")
def view_complete_medical_history(patient_id: int):
    """Aggregates all tables (Demographics, History, Cases) into a single nested payload target response"""
    try:
        # Replaces your manual SQL string JOIN statements using Supabase nested structural maps
        response = supabase.table("patients").select(
            "full_name, age, abha_number, medical_history(past_illnesses, known_allergies), patient_cases(created_at, current_symptoms, diagnosis_notes, prescription_image_url, ai_extracted_text)"
        ).eq("patient_id", patient_id).execute()
        
        return {"status": "Success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
