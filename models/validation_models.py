from fastapi import WebSocket
from pydantic import BaseModel, model_validator, Field
from typing import Optional, Self

class ChatUser(BaseModel):
    id: Optional[int] = Field(description="Number associated with the user.")
    name: str = Field(description="Name of the user.", min_length=3, max_length=10)

class UserInDB(ChatUser):
    password: str = Field(description="User password.", min_length=6, max_length=18)

    @model_validator(mode="after")
    def is_alpha_name(self) -> Self:
        if not self.name.isalpha():
            raise ValueError("Name should only consists of letters")
        
        return self

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_name: str

class User:
    '''Represents user information connected in the websocket'''

    def __init__(self, user_model: UserInDB, websocket_client: WebSocket):
        self.id = user_model.id
        self.name = user_model.name
        self.websocket_client = websocket_client


    # def set_client(self, client: WebSocket):
    #     '''
    #     Add a user websocket client.
    #     '''
    #     if client:
    #         self.websocket_client = client