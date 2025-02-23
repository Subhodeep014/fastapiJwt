from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from core.config import SECRET_KEY, ALGORITHM

async def get_current_user(request:Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=403, detail="Not Autheticated")
    
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms= [ALGORITHM])
        email: str=payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid Code")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")