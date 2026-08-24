from fastapi import APIRouter, Depends
from app.dependencies import get_current_user

router = APIRouter(
    prefix = "/employees",
    tags = ["Employees"]
)

@router.get("/")
async def get_employees(
    current_user = Depends(get_current_user)
    ):

    return {
        "message": "You can acess employees",
        "user": current_user["email"]
    }

