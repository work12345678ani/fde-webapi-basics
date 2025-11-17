from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
async def root():
  return {"hello": "world"}


@app.get("/greeting")
async def greeting():
  """General Kenobi"""
  return {"message": "hello there"}

@app.get("/health")
async def health():
  """Dummy health check endpoint that does nothing."""
  return {"status": "ok"}


@app.get("/add")
async def add(a: int, b: int):
  """Add the two numbers and return the result."""
  return {"result": a + b}

@app.get("/multiply")
async def multiply(a: int, b: int):
  """Multiply two numbers and return the result."""
  return {"result": a * b}
