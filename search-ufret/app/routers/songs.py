from fastapi import APIRouter

from app.services.estimator import estimate_song_metadata
from app.services.es import search_songs

router = APIRouter()


@router.get("/search", tags=["songs"])
def get_search(text: str):
    songs = estimate_song_metadata(text=text)
    print(f"candidates: {songs}")
    result = search_songs(songs)
    print(f"result: {result}")

    return {"result": result}
