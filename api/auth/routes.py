from fastapi import APIRouter, Depends, HTTPException, Response
from datetime import timedelta
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from auth.jwt import create_access_token
from auth.dependencies import get_current_user
from sqlalchemy.future import select
from .hashing import hash_password, verify_password
from models import User 

auth_router = APIRouter()

ACCESS_TOKEN_EXPIRE = 30

@auth_router.post("/signup")
async def signup(email:str, password:str, db:AsyncSession = Depends(get_db)):
    hashed_password = hash_password(password=password)
    user = User(email=email, hashed_password = hashed_password)
    db.add(user)
    await db.commit()
    return {"message":"User created successfully"}

@auth_router.post("/signin")
async def signin(response :Response, email:str, password:str, db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(User).where(User.email==email))
    user = result.scalars().first()
    if not user or not verify_password(password,user.hashed_password):
        raise HTTPException(status_code=401, detail="Ivalid Credential")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    access_token = create_access_token({"sub":user.email}, access_token_expires)

    response.set_cookie(
        key="access_token",
        value=access_token,
        secure=True,
        httponly=True,
        samesite="Lax"
    )
    return {"message":"Logged in successfully"}

@auth_router.get("/protected")
async def protected_route(email:str = Depends(get_current_user)):
    return {"message":f"Hello {email}, you accessed a protected route"}



    
