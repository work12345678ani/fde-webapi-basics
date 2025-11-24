from fastapi import FastAPI, HTTPException, status, Request, File, UploadFile, Form
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from modules.connector import get_db_session
from modules.config import settings
from modules.models import JobBoard, JobPosts
import os



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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

# =================================API ENDPOINTS=================================

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
# ===============================================================================

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
  indexFilePath = os.path.join("frontend", "build", "client", "index.html")
  return FileResponse(path=indexFilePath, media_type="text/html")
