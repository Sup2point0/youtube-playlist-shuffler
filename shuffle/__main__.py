import json

from config import ROOT, SCRIPT
from auth import authorise


yt = authorise()

with open(SCRIPT / "playlists.json") as source:
  playlists = json.load(source)

request = yt.playlistItems().list(
  part = "snippet",
  playlistId = playlists["Maximum Rhythm"],
)
response = request.execute()
print(response)
