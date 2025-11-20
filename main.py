from fastapi import FastAPI, HTTPException, status, Request, File, UploadFile, Form
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



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

class SPAStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        # Try normal static file handling first
        response = await super().get_response(path, scope)

        # If file not found, fall back to root index.html
        if response.status_code == 404:
            return await super().get_response("index.html", scope)

        return response



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

# @app.get("/")
# async def root(request: Request):
#     return templates.TemplateResponse(request=request, name="homepage.html", context={"jobs": combined_job_listings.keys()}) 

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/job-boards/{company_name}")
async def return_jobs(request: Request, company_name: str):
    if company_name in combined_job_listings.keys():
      return templates.TemplateResponse(request=request, name="index.html", context={"company": combined_job_listings[company_name], "companyName": company_name.capitalize(), "logo": logos.get(company_name, "")})
    else:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail="404 Company not found.")


@app.get("/api/job-boards/{company_name}")
async def return_jobs(company_name: str):
    if company_name in combined_job_listings.keys():
        return combined_job_listings[company_name]
    else:
        return JSONResponse(status_code=status.HTTP_418_IM_A_TEAPOT, content={"message": "Company not found."})
    
@app.get("/bruh")
async def test():
    return HTMLResponse("<h1>Bruh moment</h1>")

app.mount("/test", SPAStaticFiles(directory="frontend/dist", html=True), name="test")


@app.get("/admin")
async def admin_page(request: Request):
    return templates.TemplateResponse(request=request, name="admin.html", context={"Company": combined_job_listings.keys()})

@app.post("/job-boards/update-information")
async def update_information(
    company_name: str = Form(...),
    new_company_name: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile | None = None
):
    if company_name == "" and new_company_name == "":
        return HTMLResponse("<h1>Please provide a company name.</h1>", status_code=status.HTTP_400_BAD_REQUEST)
    if company_name not in combined_job_listings:
        company_name = new_company_name
        combined_job_listings[company_name] = []
    combined_job_listings[company_name].append({"title": title, "description": description})
    if file and file.filename:
        file_location = f"static/{company_name}_logo.{file.filename.split('.')[-1]}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        logos[company_name] = f"/static/{company_name}_logo.{file.filename.split('.')[-1]}"
    return RedirectResponse(url=f"/job-boards/{company_name}", status_code=status.HTTP_303_SEE_OTHER)
        