from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["healthcheck"])
def get_healthcheck():
    return {"health": "ok"}
