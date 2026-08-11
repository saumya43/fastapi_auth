from fastapi import FastAPI
from app.database import connect_database

app = FastAPI(
    Title = "discovering Oauth",
    version = "1.0.1"

)

@app.on_event("startup")
async def startup():
    await connect_database()

@app.get("/")
async def root():
   return{
    "message": "Welcome to FastAPI Authentication project"
   }
    

