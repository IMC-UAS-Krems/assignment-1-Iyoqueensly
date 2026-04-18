"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform - the hub that manages all users, tracks, artists, albums, playlist and sessions
"""

from datetime import datetime, timedelta
from .users import PremiumUser, FamilyMember
from .tracks import Song
from .playlists import CollaborativePlaylist
from collections import defaultdict #creates dictionary with default values

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
        self._track[track.track_id] = track #registers a track

    def add_album(self, album):
        self._albums[album.album_id] = album #registers an album

    def add_artist(self, artist):
        self._artists[artist.artist_id] = artist

    def add_playlist(self, playlist):
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session):
        self._sessions.append(session)
        session.user.add_session(session) #records listening session and add it to users personal history

    def add_user(self, user):
        self._users[user.user_id] = user



    """
    accesor methods - returns (track, album, artist, user) with their ids
    """
    def get_track(self, track_id):
        return self._track.get(track_id)

    def get_album(self, album_id):
        return self._albums.get(album_id)

    def get_artist(self, artist_id):
        return self._artists.get(artist_id)

    def get_user(self, user_id):
        return self._users.get(user_id)

    def all_tracks(self):
        return list(self._track.values()) #list of all track objects

    def all_users(self):
        return list(self._users.values()) #returns list of all registered user objects

    """returns total listening time in minutes for all sessions"""
    def total_listening_time_minutes(self, start: datetime, end: datetime):
        total_seconds = sum(
            sessions.duration_listened_seconds
            for sessions in self._sessions
            if start <= sessions.timestamp <= end #timestamp falls within start and end
        )
        return total_seconds / 60

    """counts distinct tracks listened to in the last days for each premium user, then
    returns the average of those counts, and 0.0 if no premium users 
    """
    def avg_unique_tracks_per_premium_user(self, days: int = 30):
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


    """
    returns the track listened to by the highest number of different users,
    returns none if there are no sessions
    """
    def track_with_most_distinct_listeners(self):
        if not self._sessions:
            return None

        listeners_per_track: dict = {}
        for session in self._sessions:
            track_id = session.track.track_id
            user_id = session.user.user_id
            if track_id not in listeners_per_track:
                listeners_per_track[track_id] = set()
            listeners_per_track[track_id].add(user_id)

        best_track_id = max(listeners_per_track, key=lambda track_id: len(listeners_per_track[track_id]))
        return self._track.get(best_track_id)


    """
    for each user subtype, create the average session duration in seconds
    returns a list of tuples, sorted, longest first
    """
    def avg_session_duration_by_user_type(self):

        duration_groups: dict = defaultdict(list) #groups session durations by class name of the user
        for session in self._sessions:
            type_name = type(session.user).__name__ #freeuser
            duration_groups[type_name].append(session.duration_listened_seconds)

        results = [] #calculates avr for each group
        for type_name, durations in duration_groups.items():
            avg = sum(durations) / len(durations)
            results.append((type_name, avg))

        results.sort(key=lambda  x: x[1], reverse= True) #sorts from longest avr to shortest
        return results

    """
    returns total listening time(min) for FamilyMember accounts whose age is strictly 
    less that age threshold, default threshold is 18
    """
    def total_listening_time_underage_sub_users_minutes(self, age_threshold = 18):

        total_seconds = 0
        for user in self._users.values():
            if isinstance(user, FamilyMember) and user.age < age_threshold: #only counts FamilyMember who are under the age threshold
                total_seconds += user.total_listening_seconds()
        return total_seconds / 60

    """
    returns top n artist ranked by total song listening time
    only song track counts (Podcast and audiobookstracks are excluded)
    returns list of tuples, highest first 
    """
    def top_artists_by_listening_time(self, n = 5):

        artist_seconds: dict = defaultdict(float)
        for session in self._sessions:
            track = session.track
            if isinstance(track, Song): #only songs have an artist
                artist_seconds[track.artist.artist_id] += session.duration_listened_seconds #accumulates secs listened per artist

        results = [] #conver to (Artist object, min) pairs
        for artist_id, seconds in artist_seconds.items():
            artist = self._artists.get(artist_id)
            if artist:
                results.append((artist, seconds / 60))

        results.sort(key=lambda x: x[1], reverse=True) #sorts highest first and returns only the top n
        return results[:n]


    """
    returns the genre that accounts for the most listening time for the given user
    returns none if the user does not exist or has no session
    """
    def user_top_genre(self, user_id):

        user = self._users.get(user_id)
        if not user or not user.sessions:
            return None #no user found or never listened to anything

        genre_seconds: dict = defaultdict(float)
        for session in user.sessions:
            genre_seconds[session.track.genre] += session.duration_listened_seconds #sums secs listened per genre

        total_seconds = sum(genre_seconds.values())
        if total_seconds == 0:
            return None

        top_genre = max(genre_seconds, key=lambda g: genre_seconds[g])
        percentage = (genre_seconds[top_genre] / total_seconds) * 100
        return top_genre, percentage #finds genre with most secs

    """
    returns all CollaborativePlaylists that contain tracks from more than threshold distinct artist
    only song tracks count
    returns playlists in registration order
    """
    def collaborative_playlists_with_many_artists(self, threshold = 3):

        results = []
        for playlist in self._playlists.values():
            if not isinstance(playlist, CollaborativePlaylist):
                continue #skips non-collab playlists

            artist_ids = set() #collect distinct artist ids from sing tracks only
            for track in playlist.tracks:
                if isinstance(track, Song):
                    artist_ids.add(track.artist.artist_id)

            if len(artist_ids) > threshold: #only include if artist count exceeds threshold
                results.append(playlist)
        return results


    """
    returns avg track count for standard playlist vs collab playlist as a dict with both keys
    returns 0.0 for a type with no instances
    """
    def avg_tracks_per_playlist_type(self):

        standard_counts = []
        collaborative_counts = []

        for playlist in self._playlists.values():
            count = len(playlist.tracks)
            if isinstance(playlist, CollaborativePlaylist): #checks CollaborativePlaylist first since it's a subclass of Playlist
                collaborative_counts.append(count)
            else:
                standard_counts.append(count)

        avg_standard = (sum(standard_counts) / len(standard_counts)
                        if standard_counts else 0) #use 0 as fallback if no playlist of that type exist
        avg_collab = (sum(collaborative_counts) / len(collaborative_counts)
                      if collaborative_counts else 0)

        return {"Playlist": avg_standard, "CollaborativePlaylist": avg_collab}


    """
    returns (user, albumtitles) for every user who has listened to every track on at least one complete album
    albums with no tracks are ignored
    """
    def users_who_completed_albums(self):

        results = []

        for user in self._users.values(): #gets set of all track ids the user has ever listened to
            listened_tracks_ids = user.unique_tracks_listened()
            completed_album_titles = []

            for album in self._albums.values():
                album_track_ids = album.track_ids() #set of track ids on the album
                if not album_track_ids:
                    continue

                if album_track_ids.issubset(listened_tracks_ids): #issubset checks if every album track was listened to
                    completed_album_titles.append(album.title)

            if completed_album_titles:
                results.append((user, completed_album_titles)) #only include users who completed at least one album
        return results