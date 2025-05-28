from fastapi import FastAPI, Query, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict
# from sqlalchemy import create_engine, Column, Integer, String, Depends
# from sqlalchemy.orm import sessionmaker, Session


# Initialize FastAPI app
app = FastAPI(
    title="Learn FastAPI",
    description="A simple API to learn FastAPI concepts",
    version="1.0.0"
)

# SQLAlchemy setup 
# DATABASE_URL = "postgresql://postgres:65JobApp!@db.wpxrwqojndtkxdrcqrmu.supabase.co:5432/postgres"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Pydatic modeels for request/response, Candidate
class Candidate(BaseModel):
    candidate_id: str
    name: str
    email: str
    job_id: str

class CandidateUpdate(BaseModel):
    email: Optional[str] = None
    job_id: Optional[str] = None

# This is our "database" - just a list in memory - cache memory
# applications: List[Candidate] = []

#creating a db connection session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()    

# @app.get("/jobs")
# def get_all_job_postings(db: Session = Depends(get_db)):
#     result = db.execute(text('SELECT * FROM "companies"'))
    
#     rows = result.fetchall()

#     #format each row as a String
#     output = []
#     for row in rows:
#         output.append(str(dict(row._mapping)))

#     return output 

# In-memory storage
applications: Dict[str, Candidate] = {}

# Helper function to check if candidate exists
def get_candidate(candidate_id: str) -> Candidate:
    if candidate_id not in applications:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application not found for candidate ID: {candidate_id}"
        )
    return applications[candidate_id]

@app.post("/applications", status_code=status.HTTP_201_CREATED)
def create_application(candidate: Candidate):
    applications[candidate.candidate_id] = candidate
    return {
        "status": "success",
        "message": f"Application submitted for {candidate.name}"
    }

@app.get("/applications")
def get_applications(
    company_name: str = Query(None, description="Filter by company name"),
    candidate_email: str = Query(None, description="Filter by candidate email")
):
    if company_name:
        return {
            "status": "success",
            "message": f"Here is your application for {company_name}"
        }
    elif candidate_email:
        return {
            "status": "success",
            "message": f"Here is your application for {candidate_email}"
        }
    else:
        return {
            "status": "success",
            "message": "Here are all of your applications"
        }

@app.get("/applications/{candidate_id}")
def get_candidate_application(candidate_id: str):
    candidate = get_candidate(candidate_id)
    return {
        "status": "success",
        "message": f"Application found for candidate ID: {candidate_id}"
    }

@app.put("/applications/{candidate_id}")
def update_application(candidate_id: str, candidate_update: CandidateUpdate):
    candidate = get_candidate(candidate_id)
    
    if candidate_update.email:
        candidate.email = candidate_update.email
    if candidate_update.job_id:
        candidate.job_id = candidate_update.job_id
    
    applications[candidate_id] = candidate
    return {
        "status": "success",
        "message": f"Application updated for candidate ID: {candidate_id}"
    }

@app.patch("/applications/{candidate_id}")
def partial_update_application(candidate_id: str, candidate_update: CandidateUpdate):
    candidate = get_candidate(candidate_id)
    
    updated_fields = []
    if candidate_update.email:
        candidate.email = candidate_update.email
        updated_fields.append("email")
    if candidate_update.job_id:
        candidate.job_id = candidate_update.job_id
        updated_fields.append("job_id")
    
    applications[candidate_id] = candidate
    return {
        "status": "success",
        "message": f"Updated {', '.join(updated_fields)} for candidate ID: {candidate_id}"
    }

@app.delete("/applications/{candidate_id}")
def delete_application(candidate_id: str):
    candidate = get_candidate(candidate_id)
    del applications[candidate_id]
    return {
        "status": "success",
        "message": f"Application deleted for candidate ID: {candidate_id}"
    }

# @app.get("/")
# def read_root():
#     return "Hello world"

#create a post endpoint called postAplication() retururn "message": "Application submitted successfully"
@app.post("/application")
def post_application():
    return {"message": "Application submitted successfully"}


#Create another POST request called applyForCandidate() -> /application/{candidate_id}
#return "Application for candidateID: 122 successfully submitted"

@app.post("/apply")
def get_application():
    return {
        "status": "success",
        "message": "Application for "+candidate_id +" successfully submitted",

    }

@app.post("/apply/{candidate_id}")
def get_application(candidate_id: str):
    return {
        "status": "success",
        "message": "Application for "+candidate_id +" successfully submitted",

    }

#add a get request to get the application for a candidate it should support query parameters like company name = str
#if query parameter is provided return only the applications for that company
#if query parameter is not provided return all applications
@app.get("/applications")
def get_applications(company_name: str = Query(None, discription = "it can be null" ), candidate_email: str = Query(None, discription = "it can be null" )):
    if company_name:
        return {
            "status": "success",
            "message": "Applications for "+company_name +" successfully retrieved",
        }
    else:
        return {
            "status": "success",
            "message": "All applications successfully retrieved",
        }
