from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from models.validation_models import UserInDB, TokenData
from scripts.database import Database
from scripts.logger import Logging
from typing import Annotated, Literal
import bcrypt
import jwt
import os

SECRET_KEY = os.getenv("HASH_SECRET_KEY")
ALGORITHM = "HS256"
db = Database()
log = Logging.getLogger()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Auth:
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        '''Check the password input if correct.'''
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


    def hash_password(password: str) -> str:
        '''Return a hashed password using bcrypt hashing algorithm.'''
        password_bytes = password.encode()
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password_bytes, salt)

        return hash.decode()
    

    def get_user_in_db(user_name: str) -> UserInDB | None:
        '''Fetch user data in the database if it exists.'''
        user = db.get_user(user_name)

        if user:
            return UserInDB.model_construct(**user)
        

    def authenticate_user(user_name: str, password: str) -> UserInDB | Literal[False]:
        '''Validate user by checking credentials in the database and verifying password.'''
        user = Auth.get_user_in_db(user_name)

        if not user:
            return False
        if not Auth.verify_password(password, user.password):
            return False

        return user
    

    def create_access_token(data: dict[str, str], expires_delta: timedelta):
        '''Create a JWT access token.'''
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + expires_delta
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        log.info(f"ACCESS TOKEN CREATED FOR {data["sub"]}: {encoded_jwt}")

        return encoded_jwt


    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
        # credentials_exception = HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Invalid authentication credentials.",
        #     headers={"WWW-Authenticate": "Bearer"},
        # )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_name = payload.get("sub")


            if not user_name:
                log.info(f"USER DOESN'T EXIST.")
                raise ValueError("User doesn't exist.")
            
            token_data = TokenData(user_name=user_name)
        except InvalidTokenError:
            raise ValueError("Invalid Token.")
        
        user = Auth.get_user_in_db(user_name=token_data.user_name)

        if not user:
            raise ValueError("User doesn't exist.")
        
        return user