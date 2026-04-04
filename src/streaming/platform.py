"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import datetime, timedelta
from enum import unique

from tests.unit_tests.conftest import premium_user
from .users import PremiumUser, FamilyAccountUser, FamilyMember, FreeUser
from .tracks import Song, AudioBookTrack, Podcast
from .playlists import Playlist, CollaborativePlaylist

class StreamingPlatform:
    def __init__(self, name):
        self.name = name

        self._track = {}
        self._albums = {}
        self._artists = {}
        self._playlists = {}
        self._sessions = []
        self._users = {}


    def add_track(self, track):
        self._track[track.track_id] = track

    def add_album(self, album):
        self._albums[album.album_id] = album

    def add_artist(self, artist):
        self._artists[artist.artist_id] = artist

    def add_playlist(self, playlist):
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session):
        self._sessions.append(session)
        session.user.add_session(session)

    def add_user(self, user):
        self._users[user.user_id] = user




    def get_track(self, track_id):
        return self._track.get(track_id)

    def get_album(self, album_id):
        return self._albums.get(album_id)

    def get_artist(self, artist_id):
        return self._artists.get(artist_id)

    def get_user(self, user_id):
        return self._users.get(user_id)

    def all_tracks(self):
        return list(self._track.values())

    def all_users(self):
        return list(self._users.values())


    def total_listening_time_minutes(self, start: datetime, end: datetime):
        total_seconds = sum(
            sessions.duration_listened_seconds
            for sessions in self._sessions
            if start <= sessions.timestamp <= end
        )
        return total_seconds / 60


    def avr_unique_tracks_per_premium_user(self, days: int = 30):
        cutoff = datetime.now() - timedelta(days = days)
        premium_users = [user for user in self._users.values() if isinstance(user, PremiumUser)]

        if not premium_users:
            return 0.0

        unique_counts = []
        for user in premium_users:
            unique_tracks = {
                session.track.track_id
                for session in user.sessions
                if session.timestamp >= cutoff
            }
            unique_counts.append(len(unique_tracks))
        return sum(unique_counts) / len(unique_counts)

