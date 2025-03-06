from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from models.validation_models import Token
from typing import Annotated
from scripts.auth import Auth
from scripts.database import Database

from scripts.logger import Logging

ACCESS_TOKEN_EXPIRES_MINUTES = 1
router = APIRouter()

log = Logging.getLogger()

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_details = Auth.authenticate_user(form_data.username, form_data.password)
    log.info(f"FETCHED DATA BY {form_data.username}: {form_data.password}")

    if not user_details:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect name or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = Auth.create_access_token(
        data={"sub": user_details.name}, 
        expires_delta=access_token_expires
    )

    return {"name": user_details.name, "token": Token(access_token=access_token, token_type="bearer")}

@router.post("/signup")
async def signup(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    hashed_password = Auth.hash_password(form_data.password)

    db = Database()

    try:
        db.add_user(data={
            "name": form_data.username, 
            "password": hashed_password
        })
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return JSONResponse({"type": "signup", "message": "Account created successfully!"})