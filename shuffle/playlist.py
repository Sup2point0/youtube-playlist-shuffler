import json
import random
from pathlib import Path


class Playlist:
  '''Represents a YouTube playlist.'''

  def __init__(self, yt, id: str):
    self.yt = yt
    self.id = id

    self.videos = None
    self.videos_prev = None


  def _check_videos_(self):
    if self.videos is None:
      raise ValueError("Playlist videos have not been fetched yet, make sure to call .fetch()")
  

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

    self._check_videos_()
    
    with open(out, "w") as dest:
      json.dump(self.videos, dest, indent = 2)


  def shuffle(self,
    freeze_start: int = None,
    freeze_end: int = None,
  ):
    '''Shuffle the videos in the playlist, keeping videos at the start and/or end frozen if specified.'''

    self._check_videos_()
    
    if freeze_start and freeze_start > len(self.videos):
      raise ValueError(f"Trying to freeze {freeze_start} videos when playlist is {len(self.videos)} long")
    
    start = self.videos[:freeze_start] if freeze_start else []
    end = self.videos[-freeze_end:] if freeze_end else []
    
    dynamic = self.videos[freeze_start:(-freeze_end if freeze_end else None)]
    random.shuffle(dynamic)
    
    self.videos_prev = self.videos.copy()
    self.videos = start + dynamic + end


  def check(self):
    '''Check if videos have been lost or duplicated during shuffling.'''

    self._check_videos_()

    current = {video["snippet"]["title"] for video in self.videos}
    previous = {video["snippet"]["title"] for video in self.videos_prev}

    if current != previous:
      print(" / warning: videos were lost during shuffling")
      print(current.difference(previous))
    elif len(self.videos) != len(self.videos_prev):
      print(" / warning: videos were duplicated during shuffling")
    else:
      print(" / checks complete, no issues found!")


  def update(self):
    '''Update the shuffled playlist through the YouTube API.'''

    self._check_videos_()

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

      try:
        request.execute()

      except Exception as e:
        print(" / failure!")
        print(e)

      else:
        print(f''' / re-indexed [{
          video['snippet']['position'] + 1
        }] -> [{
          i + 1
        }] -- {video['snippet']['title']}''')
