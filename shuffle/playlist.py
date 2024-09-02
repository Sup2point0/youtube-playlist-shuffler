import random


class Playlist:
  '''Represents a YouTube playlist.'''

  def __init__(self, yt, id):
    self.yt = yt
    self.id = id

    self.videos = None
  
  def fetch(self):
    '''Fetch the videos in the playlist through the YouTube API and store them in `.videos`.'''

    request = self.yt.playlistItems().list(
      part = "snippet",
      playlistId = self.id,
    )

    response = request.execute()
    self.videos = response["items"]

  def shuffle(self, freeze_start = None, freeze_end = None):
    '''Shuffle the videos in the playlist, keeping videos at the start and/or end frozen if specified.'''

    if freeze_start and freeze_start > len(self.videos):
      raise ValueError(f"Trying to freeze {freeze_start} videos when playlist is {len(self.videos)} long")
    
    start = self.videos[:freeze_start] if freeze_start else []
    end = self.videos[freeze_end:] if freeze_end else []
    
    dynamic = self.videos[freeze_start:freeze_end]
    random.shuffle(dynamic)
    
    self.videos = start + dynamic + end

  def save(self):
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
