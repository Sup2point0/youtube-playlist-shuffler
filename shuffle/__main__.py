print(">> running!")

import json

from config import ROOT
from auth import authorise
from playlist import Playlist


PLAYLIST = "Favourites / Johannes Bornlof"


## auth
yt = authorise()
print(" / authorised!")

## load
with open(ROOT / "data" / "playlists.json") as source:
  playlists = json.load(source)

playlist = playlists[PLAYLIST]

## shuffle
p = Playlist(yt, playlist["id"])
p.fetch()
p.save(ROOT / "data" / "playlists" / f"{PLAYLIST.replace("/", "-")}.json")

p.shuffle(
  freeze_start = playlist.get("freeze-start", None),
  freeze_end = playlist.get("freeze-end", None),
)
p.update()

print(">> done!")
