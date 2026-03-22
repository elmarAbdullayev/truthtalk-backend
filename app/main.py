from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, rooms
from app.core.database import Base, engine



app = FastAPI(
    title="TruthTalk API",
    description="Voice Discussion Platform API",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    try:
        print("🔧 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created!")
    except Exception as e:
        print(f"❌ Database error: {e}")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(rooms.router)

@app.get("/")
def root():
    return {
        "message": "TruthTalk API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}