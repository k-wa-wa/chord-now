import json

from seqlabel import Text
from seqlabel.matchers import DictionaryMatcher
from seqlabel.entity_filters import LongestMatchFilter

from app.models import SongMetadata


matcher = DictionaryMatcher()

with open("./init-data.json") as f:
    data = json.loads(f.read())

matcher.add({
    d[key]: key
    for d in data for key in ["song_name", "artist_name"]
})


def estimate_song_metadata(text: str):
    entities = matcher.match(Text(text))
    entities = LongestMatchFilter()(entities)

    def extract_candidates(label: str):
        return sorted(list(set([
            text[e.start_offset:e.end_offset+1]
            for e in entities
            if e.label == label
        ])), reverse=True)

    song_name_candidates = extract_candidates("song_name")
    artist_name_candidates = extract_candidates("artist_name")

    return [
        SongMetadata(song_name=s, artist_name=a)
        for s in song_name_candidates
        for a in artist_name_candidates
    ]
