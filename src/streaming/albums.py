"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album - a music album with tracks sorted by track number
"""



class Album():
    def __init__(self, album_id, title, artist, release_year):
        self.album_id = album_id #str
        self.title = title #str
        self.artist = artist #Artist
        self.release_year = release_year #int
        self.tracks = [] #list

    def add_track(self, track):
        self.tracks.append(track)
        self.tracks.sort(key=lambda track: track.track_number)
        track.album = self

    def track_ids(self):
        return {track.track_id for track in self.tracks}

    def duration_seconds(self):
        return sum(track.duration_seconds for track in self.tracks)