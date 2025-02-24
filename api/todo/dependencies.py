from models import User
from fastapi import Depends, HTTPException
from core.database import get_db
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
async def get_user_by_email(email: str, db: AsyncSession=Depends(get_db)):
    result = await db.execute(select(User).filter(User.email==email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")