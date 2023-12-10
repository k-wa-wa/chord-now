import os
from typing import Any
from dataclasses import dataclass

from elasticsearch import Elasticsearch

from app.models import SongMetadata


es = Elasticsearch(os.getenv("ES_ENDPOINT"))
# es.close()


@dataclass
class SearchSongsResult(SongMetadata):
    data_id: str
    score: float
    _sort_index: Any | None


def _query_metadata(query: dict):
    result: list[SearchSongsResult] = []

    r = es.search(index="ufret", query=query)
    for hit in r.body["hits"]["hits"]:
        result.append(
            SearchSongsResult(
                song_name=hit["_source"]["song_name"],
                artist_name=hit["_source"]["artist_name"],
                data_id=str(hit["_source"]["data_id"]),
                score=float(hit["_score"]),
                _sort_index=hit["sort"][0] if len(hit["sort"]) else None
            )
        )

    return result


def search_songs(metadata_list: list[SongMetadata]):
    result = []
    for metadata in metadata_list:
        query = {
            "bool": {
                "must": [
                    {
                        "match": {
                            "song_name": metadata.song_name,
                        },
                    },
                    {
                        "match": {
                            "artist_name": metadata.artist_name,
                        },
                    },
                ]
            }
        }
        r = _query_metadata(query)
        result.extend(r)

    return result


def get_all_metadata():
    result = []

    search_after = None
    while True:
        query = {
            "match_all": {},
            "search_after": [search_after] if search_after else [],
            "sort": [
                {
                    "_id": "asc"
                }
            ]
        }
        r = _query_metadata(query)
        result.extend(r)
        if len(r):
            search_after = r[-1]._sort_index
        else:
            break

    return result
