"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist - a personal ordered collection of tracks owned by a user
    - CollaborativePlaylist -  a shared playlist with multiple contributors
"""
class Playlist:
    def __init__(self, playlist_id, name, owner):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = [] #ordered list of Track objects

    def add_track(self, track): #add a track only if it is not already in playlist
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track_id): #removes track with given track_id
        self.tracks = [track for track in self.tracks if track.track_id != track_id]

    def total_duration_seconds(self):
        total = 0
        for track in self.tracks:
            total = total + track.duration_seconds
        return total

class CollaborativePlaylist(Playlist): #playlist where multiple users can contribute tracks to
    def __init__(self, playlist_id, name, owner):
        super().__init__(playlist_id, name, owner)
        self.contributors = [owner] #owner can not be removed

    def add_contributor(self, user):
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user):
        if user != self.owner and user in self.contributors:
            self.contributors.remove(user)