"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
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
        track.album = self

    def track_ids(self):
        ids = set()
        for track in self.tracks:
            ids.add(track.track_id)
        return ids
    #return {t.track_id for t in self.tracks}

    def duration_seconds(self):
        total = 0
        for track in self.tracks:
            total = total + track.duration_seconds
        return total
    #return sum(t.duration_seconds for t in self.tracks)