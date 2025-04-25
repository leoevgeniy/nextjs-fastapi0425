from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "127.0.0.1"],  # Next.js dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
