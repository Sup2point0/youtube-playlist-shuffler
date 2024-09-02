import json
import random
from pathlib import Path


class Playlist:
  '''Represents a YouTube playlist.'''

  def __init__(self, yt, id: str):
    self.yt = yt
    self.id = id

    self.videos = None
  

  def fetch(self):
    '''Fetch the videos in the playlist through the YouTube API and store them in `.videos`.'''

    self.videos = []
    init = True

    while True:
      if init:
        request = self.yt.playlistItems().list(
          part = "snippet",
          playlistId = self.id,
          maxResults = 50,
        )
        init = False

      else:
        request = self.yt.playlistItems().list(
          part = "snippet",
          playlistId = self.id,
          maxResults = 50,
          pageToken = page,
        )

      response = request.execute()
      self.videos.extend(response["items"])

      if "nextPageToken" in response:
        page = response["nextPageToken"]
      else:
        return
      

  def save(self, out: str | Path):
    '''Save the videos in the playlist to a JSON file.'''

    if self.videos is None:
      raise ValueError("Playlist videos have not been fetched yet, make sure to call .fetch()")
    
    with open(out, "w") as dest:
      json.dump(self.videos, dest, indent = 2)


  def shuffle(self,
    freeze_start: int = None,
    freeze_end: int = None,
  ):
    '''Shuffle the videos in the playlist, keeping videos at the start and/or end frozen if specified.'''

    if self.videos is None:
      raise ValueError("Playlist videos have not been fetched yet, make sure to call .fetch()")
    
    if freeze_start and freeze_start > len(self.videos):
      raise ValueError(f"Trying to freeze {freeze_start} videos when playlist is {len(self.videos)} long")
    
    start = self.videos[:freeze_start] if freeze_start else []
    end = self.videos[freeze_end:] if freeze_end else []
    
    dynamic = self.videos[freeze_start:freeze_end]
    random.shuffle(dynamic)
    
    self.videos = start + dynamic + end


  def update(self):
    '''Update the shuffled playlist through the YouTube API.'''

    for i, video in enumerate(self.videos):
      request = self.yt.playlistItems().update(
        part = "snippet",
        body = {
          "id": video["id"],
          "snippet": {
            "playlistId": self.id,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": video["snippet"]["resourceId"]["videoId"]
            },
            "position": i,
          },
        },
      )

      request.execute()
      print(f''' / re-indexed [{
        video['snippet']['position'] + 1
      }] -> [{
        i + 1
      }] - {video['snippet']['title']}''')
