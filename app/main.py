from fastapi import FastAPI
from app.database import connect_database
from app.routers.auth import router as auth_router
from app.routers.employee import router as employee_router

app = FastAPI(
    Title = "discovering Oauth",
    version = "1.0.1"

)

app.include_router(auth_router)
app.include_router(employee_router)

@app.on_event("startup")
async def startup():
    await connect_database()

@app.get("/")
async def root():
   return{
    "message": "Welcome to FastAPI Authentication project"
   }
    

