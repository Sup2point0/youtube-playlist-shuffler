print(">> running!")

import json

from config import ROOT
from auth import authorise
from playlist import Playlist


## auth
yt = authorise()
print(" / authorised!")

## load
with open(ROOT / "data" / "playlists.json") as source:
  playlists = json.load(source)

choice = playlists["choice"]
playlist = playlists[choice]

## shuffle
p = Playlist(yt, playlist["id"])
p.fetch()
p.save(ROOT / "data" / "playlists" / f"{choice.replace("/", "-")}.json")

p.shuffle(
  freeze_start = playlist.get("freeze-start", None),
  freeze_end = playlist.get("freeze-end", None),
)
p.update()

print(">> done!")
