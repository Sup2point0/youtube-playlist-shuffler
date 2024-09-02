print(">> running!")

import json

from config import ROOT, SCRIPT
from auth import authorise
from playlist import Playlist


yt = authorise()
print(" / authorised!")

with open(SCRIPT / "playlists.json") as source:
  playlists = json.load(source)


p = Playlist(yt, playlists["Maximum Rhythm"])
p.fetch()
p.save(ROOT / "data" / "Maximum Rhythm.json")

print("BEFORE =", len(p.videos))
for video in p.videos[:9]:
  print(video['snippet']['title'])

p.shuffle(freeze_start = 3)

print("AFTER =", len(p.videos))
for video in p.videos[:9]:
  print(video['snippet']['title'])
p.update()

print(">> done!")
