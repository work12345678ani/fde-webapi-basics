from fastapi import Depends, FastAPI, HTTPException, status, Request, File, UploadFile, Form, Response, Cookie
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from modules.connector import get_db_session
from modules.config import settings
from modules.models import JobBoard, JobPosts, JobApplications
from pydantic import BaseModel, Field, field_validator
from modules.file_storage import upload_file
from modules.auth import authenticate_admin, is_admin #type: ignore
import os



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
if not settings.PRODUCTION:
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



combined_job_listings = {
    "acme": [
        {"title": "Software Engineer", "description": "Develop and maintain software applications."},
        {"title": "Data Scientist", "description": "Analyze complex data to support business decisions and build predictive models."},
        {"title": "Product Manager", "description": "Define product vision, manage roadmaps, and coordinate cross-functional teams to deliver features."},
    ],
    "bcg": [
        {"title": "Consultant", "description": "Advise clients, analyze business problems, and develop strategic solutions."},
        {"title": "Business Analyst", "description": "Gather requirements, evaluate processes, and provide data-driven recommendations."},
        {"title": "Project Manager", "description": "Plan, execute, and oversee projects to ensure timely and successful delivery."},
    ],
    "atlas": [
        {"title": "DevOps Engineer", "description": "Build and maintain CI/CD pipelines, automate infrastructure, and improve deployment reliability."},
        {"title": "Cloud Architect", "description": "Design cloud environments, ensure scalability, and guide cloud adoption strategy."},
    ]
}

logos = {
    "acme": "/static/acme_logo.jpg",
    "bcg": "/static/bcg_logo.jpg",
    "atlas": "/static/atlas_logo.png"
}


app.mount("/assets", StaticFiles(directory="frontend/build/client/assets"))

def is_admin_user(admin_session: str | None = Cookie(default=None)):
    if not admin_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Logged in.",
        )
    if not is_admin(admin_session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin session.",
        )
    return "authenticated"


#=================================PYDANTIC CLASSES=================================

class NewCompany(BaseModel):
    id: int
    slug: str
    logo: UploadFile = File(...)

class UpdateCompany(BaseModel):
    slug: str
    logo: UploadFile = File(...)

class JobApplication(BaseModel):
    first_name: Annotated[str, Form()]
    last_name: Annotated[str, Form()]
    email: Annotated[str, Form()]
    job_id: Annotated[int, Form()]
    resume: UploadFile = File(...)

class DeleteCompany(BaseModel):
    slug: str

class AdminLoginForm(BaseModel):
   username : str
   password : str

# =================================API ENDPOINTS=================================



@app.post("/api/admin-login")
async def admin_login(response: Response, admin_login_form: Annotated[AdminLoginForm, Form()]):
   auth_response = authenticate_admin(admin_login_form.username, admin_login_form.password)
   if auth_response is not None:
      secure = settings.PRODUCTION
      response.set_cookie(key="admin_session", value=auth_response, httponly=True, secure=secure, samesite="Lax")
      return {}
   else:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@app.get("/api/job-boards")
async def get_job_boards():
    """Return all job boards from the database"""
    with get_db_session() as session:
        jobBoards = session.query(JobBoard).all()
        return jobBoards

@app.get("/api/health")
async def health_check():
    """Checks if the database connection is healthy"""
    with get_db_session() as session:
        try:
            session.execute(text("SELECT 1"))
            return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "OK"})
        except:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "Database connection failed."})

@app.get("/api/job-boards/{company_name}/job-posts")
async def return_jobs(company_name: str):
    """Return all jobs for a specific company. Returns 418 if the company is not found"""
    with get_db_session() as session: 
        job_posts = (
            session.query(JobPosts)
            .join(JobBoard, JobPosts.company_id == JobBoard.id)
            .filter(JobBoard.slug == company_name)
            .all()
        )

        if not job_posts:
            raise HTTPException(
                status_code=status.HTTP_418_IM_A_TEAPOT,
                detail={"detail": "Company not found."},
            )

        return [
            {
                "id": job.id,
                "title": job.title,
                "description": job.description,
                "location": job.location,
            }
            for job in job_posts
        ]
@app.get("/api/job-boards/{company_name}")
async def get_company_details(company_name: str):
    with get_db_session() as session:
        company = session.query(JobBoard).filter(JobBoard.slug==company_name).first()
        if not company:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": "Error", "message":"Company not found"})
        return JSONResponse(content={"slug": company.slug, "logo_url": company.logo_url, "id": company.id})

@app.get("/api/job-applications")
async def get_job_applications():
    with get_db_session() as session:
        job_applications = (
            session.query(JobApplications).all()
        )

        return [
            {
                "id" :app.id,
                "job_id": app.job_post_id,
                "first_name": app.first_name,
                "last_name": app.last_name,
                "email": app.email,
                "resume_loc": app.resume_loc
            }
            for app in job_applications
        ]

@app.post("/api/job-applications")
async def apply_for_job(applicant: Annotated[JobApplication, Form()]):
    try:
        with get_db_session() as session:
            isOpen = session.query(
                JobPosts.isOpen
            ).filter(JobPosts.id == applicant.job_id).scalar()

            if not isOpen:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status":"error", "message":"Application does not exist or is no longer accepting new applicants"})

            resume_content = await applicant.resume.read()

            resume_path = upload_file("resumes", applicant.resume.filename, resume_content, applicant.resume.content_type)

            row = JobApplications(
                job_post_id = applicant.job_id,
                first_name = applicant.first_name, 
                last_name = applicant.last_name, 
                email = applicant.email,
                resume_loc = resume_path
            )
            session.add(row)
            session.commit()

            return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "ok", "message":"Successfully uploaded"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": e})     

@app.post("/api/job-boards")
async def add_job_board(details: Annotated[NewCompany, Form()], admin=Depends(is_admin_user)):
    contents = await details.logo.read()
    file_path = upload_file("logos", details.logo.filename, contents, details.logo.content_type)
    with get_db_session() as session:
        row = JobBoard(
            id=details.id,
            slug=details.slug,
            logo_url=file_path
        )
        session.add(row)
        session.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": file_path})

@app.put("/api/job-boards/update")
async def update_company_logo(details: Annotated[UpdateCompany, Form()], admin=Depends(is_admin_user)):
    with get_db_session() as session:
        company = session.query(JobBoard).filter(JobBoard.slug == details.slug).first()
        if not company:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status": "Error", "message":"Company not found"})
        file_content = await details.logo.read()
        if not details.logo.content_type.startswith("image/"):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"status":"Error", "message":"Not an image"})
        company.logo_url = upload_file("logos", details.logo.filename, file_content, details.logo.content_type)
        session.commit()
        session.refresh(company)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"status":"ok", "messaage":"successfully updated"})


@app.delete("/api/job-boards/{slug}/delete")
async def delete_job_board(slug: str, admin=Depends(is_admin_user)):
    with get_db_session() as session:
        job_board = session.query(JobBoard).filter_by(slug=slug).first()
        if job_board:
            session.delete(job_board)
            session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK, content={"status":"ok", "messaage":"successfully deleted"})
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"status":"error", "messaage":"Company not found"})

# ===============================================================================

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
  indexFilePath = os.path.join("frontend", "build", "client", "index.html")
  return FileResponse(path=indexFilePath, media_type="text/html")
