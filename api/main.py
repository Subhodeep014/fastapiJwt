import uvicorn
from fastapi import FastAPI
from core.database import engine
from models import Base
from contextlib import asynccontextmanager
from auth.routes import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI): 
    # Startup logic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown logic (if any)
    # For example, closing database connections
app = FastAPI(title="Auth API with JWT", lifespan=lifespan)

@app.get("/")
def Home():
    return {"message":"Welcome to the auth api"}

app.include_router(auth_router, prefix="/auth")
