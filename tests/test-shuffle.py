from shuffle.playlist import Playlist


p = Playlist(yt = None, id = "test")


def test_shuffle():
  p.videos = list(range(10))

  p.shuffle()
  assert p.videos != [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def test_shuffle_with_freeze():
  p.videos = list(range(10))
  
  p.shuffle(freeze_start = 3)
  assert p.videos[:3] == [0, 1, 2]
  assert p.videos[3:] != [3, 4, 5, 6, 7, 8, 9]

  p.videos = list(range(10))
  p.shuffle(freeze_end = 2)
  assert p.videos[:7] != [0, 1, 2, 3, 4, 5, 6, 7]
  assert p.videos[-2:] == [8, 9]
