

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.songs import router as songs_router
from app.routers.healthcheck import router as healthcheck_router

app = FastAPI()

app.include_router(songs_router, prefix="/songs")
app.include_router(healthcheck_router, prefix="/healthcheck")

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
