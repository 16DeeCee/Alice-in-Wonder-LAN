from dotenv import  load_dotenv, find_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from routes import ws_router, auth_router
import os

_ = load_dotenv(find_dotenv())

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

app.include_router(ws_router.router)
app.include_router(auth_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, reload=True)