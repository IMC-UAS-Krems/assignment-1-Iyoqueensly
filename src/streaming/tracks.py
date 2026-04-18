"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class) - can not be created directly
    - Song - a music track linked to an Artist
      - SingleRelease - a Song released independently with a release date
      - AlbumTrack - a Song that belongs to an Album with a track number
    - Podcast - a podcast episode with a host and description
      - InterviewEpisode - a serialised podcast with season/episode numbers
      - NarrativeEpisode - a podcast episode featuring a named guest
    - AudiobookTrack - an audiobook chapter with an author and narrator
"""

from abc import ABC #abstract base class, prevents direct instantiation

class Track(ABC):
    def __init__(self, track_id, title, duration_seconds, genre):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self):
        return self.duration_seconds / 60

    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id


class Song(Track):
    def __init__(self, track_id, title, duration_seconds, genre, artist):
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist

class AlbumTrack(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, track_number, album=None):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.track_number = track_number #position on the album (1, 2, 3)
        self.album = album # Album object, set later when added to album

class SingleRelease(Song):
    def __init__(self, track_id, title, duration_seconds, genre, artist, release_date):
        super().__init__(track_id, title, duration_seconds, genre,  artist)
        self.release_date = release_date #date of release with datetime.date

class Podcast(Track):
    def __init__(self, track_id, title, duration_seconds,  genre, host, description = ""):
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host #podcast host name
        self.description = description #summary of episode

class NarrativeEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds,  genre, host, season, episode_number, description = ""):
        super().__init__(track_id, title, duration_seconds, genre, host, description)
        self.season = season #season episode belongs to
        self.episode_number = episode_number #within the season

class InterviewEpisode(Podcast):
    def __init__(self, track_id, title, duration_seconds,  genre, host, guest, description = ""):
        super().__init__(track_id, title, duration_seconds,  genre, host, description)
        self.guest = guest #guest on the podcast being interviewed


class AudiobookTrack(Track):
    def __init__(self, track_id, title, duration_seconds, genre, author, narrator):
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator #who is reading the book aloud


