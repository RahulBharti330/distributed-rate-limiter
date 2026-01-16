from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["user"])


@router.get("/data")
def get_data():
    return {"message": "User data response"}
