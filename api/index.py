from fastapi import FastAPI, Request, HTTPException
from starlette.staticfiles import StaticFiles
from sqladmin import Admin
from api.database.database import engine
from api.admin.userAdmin import UserAdmin
from api.auth.auth import authentication_backend
from api.routers.users import router as router_users
from api.routers.chat import router as router_chat
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.middleware import limiter, logger
from slowapi.middleware import SlowAPIMiddleware
import datetime

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация лимитера
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


admin = Admin(app, engine, authentication_backend=authentication_backend, base_url='/api/admin')

admin.add_view(UserAdmin)

    
app.include_router(router_users)
app.include_router(router_chat)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers if hasattr(exc, "headers") else None
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.datetime.now()
    response = await call_next(request)
    process_time = (datetime.datetime.now() - start_time).total_seconds() * 1000
    
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Time: {process_time:.2f}ms"
    )
    
    return response
app.mount("/static", StaticFiles(directory="static"), name="static")
