"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
class Playlist:
    def __init__(self, playlist_id, name, owner):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = []

    def add_track(self, track):
        self.tracks.append(track)

    def remove_track(self, track_id):
        self.tracks.remove(track_id)

    def total_duration(self):
        total = 0
        for track in self.tracks:
            total = total + track.duration_seconds
        return total

class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, name, owner, contributors):
        super().__init__(playlist_id, name, owner)
        self.contributors = contributors

    def add_contributor(self, user):
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user):
        if user in self.contributors:
            self.contributors.remove(user)