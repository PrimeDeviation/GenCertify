import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO")
log_file = os.getenv("LOG_FILE", "logs/app.log")
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Import routers
from app.api.static_input import router as static_input_router
from app.api.chat import router as chat_router
from app.api.evaluation import router as evaluation_router
from app.api.documents import router as documents_router

# Create FastAPI app
app = FastAPI(
    title="GenCertify",
    description="A Certification Readiness and Document Drafting Tool",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(static_input_router, prefix="/api/static-input", tags=["Static Input"])
app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])
app.include_router(evaluation_router, prefix="/api/evaluation", tags=["Evaluation"])
app.include_router(documents_router, prefix="/api/documents", tags=["Documents"])

# Root endpoint
@app.get("/")
async def root(request: Request):
    logger.info("Root endpoint accessed")
    return templates.TemplateResponse("index.html", {"request": request, "now": datetime.now().strftime("%H:%M:%S")})

# Login endpoint
@app.get("/login")
async def login_page(request: Request):
    logger.info("Login page accessed")
    return templates.TemplateResponse("login.html", {"request": request})

# Register endpoint
@app.get("/register")
async def register_page(request: Request):
    logger.info("Register page accessed")
    return templates.TemplateResponse("register.html", {"request": request})

# Error page
@app.get("/error/{status_code}")
async def error_page(request: Request, status_code: int, message: str = "An error occurred"):
    logger.info(f"Error page accessed with status code {status_code}")
    return templates.TemplateResponse(
        "error.html", 
        {"request": request, "status_code": status_code, "message": message}
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    logger.debug("Health check endpoint accessed")
    return {"status": "healthy"}

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."},
    )

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    logger.info(f"Starting GenCertify application on {host}:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=True) 