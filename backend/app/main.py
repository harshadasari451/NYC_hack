from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import upload, chat, persona


app = FastAPI(
    title=settings.APP_NAME,
    description="Interactive AI Avatar — Mother-Daughter Conversation Platform",
    version="0.1.0",
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(persona.router, prefix="/api/persona", tags=["Persona"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
