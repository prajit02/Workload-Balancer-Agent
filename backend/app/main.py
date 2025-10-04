from fastapi import FastAPI
from app.routes import workitems
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Workload Balancing Agent MCP")

app.include_router(workitems.router)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Workload Balancing Agent MCP API"}