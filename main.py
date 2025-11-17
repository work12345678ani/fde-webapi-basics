from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
async def root():
  return {"hello": "world"}

@app.get("/health")
async def health():
  return {"status": "ok"}