from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyHeader
from jose import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
import httpx
from app.config import settings

router = APIRouter()

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm="HS256")
    return encoded_jwt

async def get_current_user(token: str = Depends(api_key_header)):
    if not token:
        raise HTTPException(status_code=401, detail="Canvas token is missing")
    return token

@router.post("/token")
async def login(canvas_token: str):
    # Verify the Canvas token by making a request to the Canvas API
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.CANVAS_API_BASE_URL}/users/self",
            headers={"Authorization": f"Bearer {canvas_token}"}
        )
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Canvas token")
    
    # If the Canvas token is valid, create our own access token
    access_token = create_access_token(data={"sub": canvas_token})
    return {"access_token": access_token, "token_type": "bearer"}